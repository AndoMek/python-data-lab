import math
import os
import re
from contextlib import closing

import boto3
import psycopg2
from psycopg2.extras import DictCursor

from lambda_helpers import lambda_logger, packages_info, func_logger

# Get script directory
ROOT = os.path.abspath(os.path.dirname(__file__))

# Setup logger
LOGGER = lambda_logger(
    custom_logger=True,
    log_level=os.environ.get("LOG_LEVEL", "DEBUG"),
)
LOGGER.debug(packages_info())

SSM_URL_PATTERN = re.compile(r"^(ssm://)([a-zA-Z0-9_./-]+)$")


def get_ssm_key(ssm_name, region_name: str = None, session: boto3.session.Session = None):
    """ Get AWS System Manager Parameter Store (SSM) values

    Args:
        ssm_name: string
        region_name: string
        session: boto3.session.Session

    Returns:
        SSM value
    """
    session = session or boto3.session.Session()
    region_name = region_name or session.region_name or "eu-west-1"
    client = session.client("ssm", region_name=region_name)

    response = client.get_parameter(Name=ssm_name, WithDecryption=True)
    return response["Parameter"]["Value"]


@func_logger(LOGGER)
def calc_workers(workers, aws_lambda_memory):
    if workers:
        return workers

    if aws_lambda_memory:
        cores = aws_lambda_memory / 1792
    else:
        cores = (os.cpu_count() or 1)

    if cores < 5:
        return math.ceil(cores * 8)
    else:
        return 32


@func_logger(LOGGER)
def lambda_handler(event, context):
    try:
        aws_lambda_memory = int(context.memory_limit_in_mb)
    except (AttributeError, TypeError):
        aws_lambda_memory = None

    workers = calc_workers(event.get("workers"), aws_lambda_memory)
    LOGGER.info("Workers: %s" % workers)

    connection_string = event.get("db_connect") or os.environ.get("DB_CONNECT")
    if not connection_string:
        return {"code": 400, "message": "Bad Request"}

    m = SSM_URL_PATTERN.match(connection_string)
    if m:
        connect_url = get_ssm_key(m.expand("\\2"))
    else:
        connect_url = connection_string

    try:
        with closing(psycopg2.connect(connect_url)) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT version() as version;")
                result = cursor.fetchone()
    except Exception:
        return {"code": 500, "message": "Internal Server Error"}
    else:
        return {"code": 200, "message": dict(result)}
