#!/usr/bin/env bash
set -e

# This is old method of build lambda. Please use something like AWS CodeBuild & CodePipeline

cd ${1:-${PWD}}

build_directory=$(readlink -f build)
dist_directory=$(readlink -f dist)

rm -fr ${build_directory}
mkdir ${build_directory} -p
mkdir ${dist_directory} -p

for lambda in $(find . -maxdepth 1 -name "lambda*" -type d); do

  lambda=$(readlink -f $lambda)
  name=$(echo $lambda | sed 's/.*lambda_//' | sed 's/_/-/g')

  # Build Lambda Code
  lambda_dir="${build_directory}/lambda-${name}"
  mkdir "${lambda_dir}" -p
  cp -r $lambda/* "${lambda_dir}"
  rm -f "${lambda_dir}/__init__.py"
  cp ./lambda_helpers.py "${lambda_dir}"
  find "${build_directory}/lambda-${name}" -name '*.py' -exec chmod 755 {} +

  # Build Lambda Dependencies
  if [ -f "$lambda/requirements.txt" ]; then
      virtualenv -p python3.8 "${build_directory}/venv-${name}"
      source "${build_directory}/venv-${name}/bin/activate"
      pip install --target="${lambda_dir}" -r $lambda/requirements.txt
      deactivate
  fi

  # Prepare sources
  sources=($lambda_dir)

  for source_dir in "${sources[@]}"; do
    find "${source_dir}" -name '*.pyc' -exec rm -f {} +
    find "${source_dir}" -name '*.pyo' -exec rm -f {} +
    find "${source_dir}" -name '*~' -exec rm -f {} +
    find "${source_dir}" -name '__pycache__' -exec rm -fr {} +
    # Change files and directories modification timestamp for idempotent build
    find "${source_dir}" -exec touch -a -m -t 201901010000.00 {} +
  done

  # Make Lambda Code Distribution
  cd "${lambda_dir}"
  find . -mindepth 1 -type f -exec zip -q -9 "${dist_directory}/lambda-${name}.zip" {} +

done
