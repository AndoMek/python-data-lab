import argparse
import logging
import os
import re
from contextlib import closing
from functools import wraps
from logging.config import dictConfig

import boto3
import psycopg2
import yaml
from flask import Flask, request
from flask_restx import Api, Resource, fields
from psycopg2.extras import DictCursor

SSM_URL_PATTERN = re.compile(r"^(ssm://)([a-zA-Z0-9_./-]+)$")

logger = logging.getLogger(__name__)
app = Flask(__name__)  # Setup new Flask application, __name__ use as Sample


class LowerThanFilter(logging.Filter):
    def __init__(self, level):
        super().__init__()

        if isinstance(level, int):
            self.level = level
        elif isinstance(level, str):
            self.level = getattr(logging, level.upper())
        else:
            raise TypeError("level expected int or string but got %r" % type(level))

    def filter(self, record):
        return record.levelno < self.level


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


def check_authorization(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            token = request.headers["X-AWESOME-API-KEY"]
        except KeyError:
            token = None

        if not token:
            return {"message": "Token is missing."}, 401

        # IRL get token value from some other resource: memcache, redis, RDBMS and etc
        # But it's ok for Mock server
        if token != "AWESOME-TOKEN":
            return {"message": "Wrong Token."}, 401

        return func(*args, **kwargs)

    return wrapper


# For authorization use dictionary with a Swagger Authorizations declaration
# https://swagger.io/docs/specification/authentication/
# !!! This dictionary only for swagger. Not for actual autorization !!!
authorizations = {
    "apikey": {
        "type": "apiKey",
        "in": "header",
        "name": "X-AWESOME-API-KEY"
    }
}

api = Api(  # Create new REST-Api and assign to Flask application
    app=app,
    title="Awesome REST-API",
    version="0.0.1",
    description="This is Awesome API on AWS",
    authorizations=authorizations,  # Pass authorizations dictionary
)

public_ns = api.namespace(
    "public_endpoints",
    description="This Is Public Endpoints"
)
private_ns = api.namespace(
    "private_endpoints",
    description="This Is Private Endpoints. Authentification Required",
    decorators=[check_authorization]
)

model = api.model(
    "Second Endpoint Data Model",
    {
        "value": fields.String(required=True, description="Awesome Value"),
    }
)

second_endpoints_ids = {  # We store data into global variables it's not recommended IRL
    1: "Spam",
    2: "Egg",
}


@public_ns.doc(responses={200: "OK", 400: "Bad Request", 500: "Internal Server Error"})
@public_ns.route("/first_endpoint")
class FirstEndpoint(Resource):
    def get(self):
        return {
            "result": 42
        }


@private_ns.doc(security="apikey")
@private_ns.route("/second_endpoint/<int:value_id>")
class SecondEndpoint(Resource):
    @private_ns.doc(responses={200: "OK", 201: "Created", 400: "Bad Request",
                               401: "Unauthorized", 500: "Internal Server Error"})  # Add documentation for codes
    @api.expect(model)  # Set expect API model
    def put(self, value_id):  # Same argument as described on decorator
        payload = request.json  # use Flask request object and parse JSON request

        # If update than return 200, if create return 201
        status = 200 if value_id in second_endpoints_ids else 201

        second_endpoints_ids[value_id] = payload["value"]
        return {value_id: second_endpoints_ids[value_id]}, status

    @private_ns.doc(responses={200: "OK", 400: "Bad Request", 401: "Unauthorized",
                               404: "Record Not Found", 500: "Internal Server Error"})
    def get(self, value_id):
        try:
            # Try return value from variable
            # IRL use some more appropriate way like RDBMS, key-value storage, and etc.
            return {value_id: second_endpoints_ids[value_id]}
        except KeyError:
            # return (response, status_code)
            return "Record Not Found", 404


@public_ns.doc(responses={200: "OK", 400: "Bad Request", 500: "Internal Server Error"})  # Add documentation for codes
@public_ns.route("/third_endpoint")
class ThirdEndpoint(Resource):
    def post(self):
        # return (response, status_code, additional-headers)
        return None, 200, {"X-AWESOME-API-KEY": "AWESOME-TOKEN"}


@private_ns.doc(security="apikey")
@private_ns.doc(responses={200: "OK", 400: "Bad Request", 500: "Internal Server Error"})
@private_ns.route("/db_endpoint")
class FourthEndpoint(Resource):
    def get(self):
        try:
            url = self.api.app.config["DB_CONNECT"]
        except KeyError:
            return "Something went wrong", 500

        with closing(psycopg2.connect(url)) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cursor:
                cursor.execute("SELECT version() as version;")
                result = cursor.fetchone()
                return dict(result)


def config_logging(verbose=0):
    if not verbose or verbose < 0:
        return

    root_directory = os.path.dirname(__file__)
    if verbose == 1:
        config_file = os.path.join(root_directory, "logging_info.yml")
    elif verbose == 2:
        config_file = os.path.join(root_directory, "logging_debug.yml")
    else:
        config_file = os.path.join(root_directory, "logging_trace.yml")

    with open(config_file) as conf:
        dictConfig(yaml.safe_load(conf))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "dbconnect", type=str, const=None,
        help="Database Connection URL", metavar="URL | SSM"
    )
    parser.add_argument(
        '-v', '--verbose', action='count', default=0
    )

    arguments = parser.parse_args()
    config_logging(arguments.verbose)

    m = SSM_URL_PATTERN.match(arguments.dbconnect)
    if m:
        app.config["DB_CONNECT"] = get_ssm_key(m.expand("\\2"))
    else:
        app.config["DB_CONNECT"] = arguments.dbconnect
    app.run(host="0.0.0.0", port="5000")


if __name__ == "__main__":
    main()
