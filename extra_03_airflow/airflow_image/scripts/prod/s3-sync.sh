#!/usr/bin/env bash
set -euo pipefail

if [ -z ${AIRFLOW__S3_PATH+x} ]; then
  echo "'AIRFLOW__S3_PATH' is unset"
  exit 1
fi

DIRECTORY="${AIRFLOW_HOME:-/opt/airflow}/dags"
CONTAIN="${AIRFLOW__S3_CONTAIN:-latest}"
INCLUDE_PATTERN="*${CONTAIN}*.zip"

S3_DAGS_ARCHIVE=$(mktemp frostbolt-dags.XXXXXXXXXX -utd)
mkdir -p "${S3_DAGS_ARCHIVE}"
EVERY=$((1*60))

echo "Sync Dags from ${AIRFLOW__S3_PATH} with pattern ${INCLUDE_PATTERN} every ${EVERY} seconds"
while true; do
  echo "Start sync Dags"
  seconds=$(( $(date -u +%s) % EVERY))

  cd "${S3_DAGS_ARCHIVE}"
  aws s3 sync "${AIRFLOW__S3_PATH}" . --exclude "*" --include "${INCLUDE_PATTERN}" --exact-timestamps
  FILE=$(find . -type f -wholename "${INCLUDE_PATTERN}" -printf '%T@ %p\n' | sort -n | tail -1 | cut -f2- -d" ")
  BASE_NAME="$(basename -- $FILE)"
  DIR_NAME="$(dirname -- $FILE)"

  cd "${DIR_NAME}"
  if [ ! -f "${DIRECTORY}/${BASE_NAME}.md5" ]; then
    echo "00000000000000000000000000000000  $BASE_NAME" > "${DIRECTORY}/${BASE_NAME}.md5"
  fi

  if ! md5sum -c "${DIRECTORY}/${BASE_NAME}.md5" --status; then
    TMP_DIR=$(mktemp frostbolt-dags.XXXXXXXXXX -utd)
    mkdir -p "${TMP_DIR}"
    unzip ${BASE_NAME} -d "${TMP_DIR}"
    rsync -avh "${TMP_DIR}/" ${DIRECTORY} --delete
    rm -fr "${TMP_DIR}"
    md5sum "${BASE_NAME}" | tee "${DIRECTORY}/${BASE_NAME}.md5"
  else
    echo "Nothing to sync"
  fi

  sleep $((EVERY - seconds))
done
