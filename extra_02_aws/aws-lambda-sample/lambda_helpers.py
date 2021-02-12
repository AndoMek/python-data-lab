import datetime
import decimal
import inspect
import json
import logging
import os
import time
import uuid
from collections.abc import Mapping, Sequence

import pkg_resources


AWS_LAMBDA_DEFAULT_LOGGING_FORMAT = "[%(levelname)s]\t%(asctime)s.%(msecs)dZ\t%(aws_request_id)s\t%(name)s\t%(message)s"
try:
    from bootstrap import LambdaContext, ClientContext, Client, CognitoIdentity

    AWS_LAMBDA_ENVIRONMENT = True
except ModuleNotFoundError:
    AWS_LAMBDA_ENVIRONMENT = False

    class ClientContext(object):
        __slots__ = ['custom', 'env', 'client']


    class Client(object):
        __slots__ = ["installation_id", "app_title", "app_version_name", "app_version_code", "app_package_name"]


    class CognitoIdentity(object):
        __slots__ = ["cognito_identity_id", "cognito_identity_pool_id"]


    def make_obj_from_dict(_class, _dict, fields=None):
        if _dict is None:
            return None
        obj = _class()
        set_obj_from_dict(obj, _dict)
        return obj


    def set_obj_from_dict(obj, _dict, fields=None):
        if fields is None:
            fields = obj.__class__.__slots__
        for field in fields:
            setattr(obj, field, _dict.get(field, None))


    class LambdaContext(object):
        def __init__(self, invoke_id, client_context, cognito_identity, epoch_deadline_time_in_ms,
                     invoked_function_arn=None):
            self.aws_request_id = invoke_id
            self.log_group_name = os.getenv("AWS_LAMBDA_LOG_GROUP_NAME")
            self.log_stream_name = os.getenv('AWS_LAMBDA_LOG_STREAM_NAME')
            self.function_name = os.getenv("AWS_LAMBDA_FUNCTION_NAME")
            self.memory_limit_in_mb = os.getenv('AWS_LAMBDA_FUNCTION_MEMORY_SIZE')
            self.function_version = os.getenv('AWS_LAMBDA_FUNCTION_VERSION')
            self.invoked_function_arn = invoked_function_arn

            self.client_context = make_obj_from_dict(ClientContext, client_context)
            if self.client_context is not None:
                self.client_context.client = None
            self.identity = None

        def get_remaining_time_in_millis(self):
            return None

        def log(self, msg):
            str_msg = str(msg)
            print(str_msg)


def utcnow():
    return datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)


def lambda_context_deserializer(context: LambdaContext):
    def deserialize(o):
        if isinstance(o, (ClientContext, CognitoIdentity, Client)):
            return {x: getattr(o, deserialize(x)) for x in o.__slots__}
        return o

    return {
        "aws_request_id": context.aws_request_id,
        "log_group_name": context.log_group_name,
        "log_stream_name": context.log_stream_name,
        "function_name": context.function_name,
        "memory_limit_in_mb": context.memory_limit_in_mb,
        "function_version": context.function_version,
        "invoked_function_arn": context.invoked_function_arn,
        "client_context": deserialize(context.client_context),
        "identity": deserialize(context.identity),
    }


class AwsJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder"""

    def default(self, o):
        """
        Extend json.JSONEncoder.default method

        :param o: object to encode
        :return: encoded object
        """
        if isinstance(o, datetime.datetime):
            return o.strftime("%Y-%m-%d %H:%M:%S.%f")
        if isinstance(o, datetime.date):
            return o.strftime("%Y-%m-%d")
        if isinstance(o, decimal.Decimal):
            if o % 1 != 0:
                return float(o)
            else:
                return int(o)
        if isinstance(o, set):
            return list(o)
        if isinstance(o, LambdaContext):
            return {
                "aws_request_id": o.aws_request_id,
                "log_group_name": o.log_group_name,
                "log_stream_name": o.log_stream_name,
                "function_name": o.function_name,
                "memory_limit_in_mb": o.memory_limit_in_mb,
                "function_version": o.function_version,
                "invoked_function_arn": o.invoked_function_arn,
                "client_context": o.client_context,
                "identity": o.identity,
            }
        if isinstance(o, (ClientContext, CognitoIdentity, Client)):
            return {x: getattr(o, x) for x in o.__slots__}
        return super().default(o)


def json_serializable_object(o):
    return json.loads(AwsJSONEncoder().encode(o))


def json_serializable_output(function):
    def wrapper(*args, **kwargs):
        return json_serializable_object(function(*args, **kwargs))

    return wrapper


PACKAGES = [str(d).split(" ")[0] for d in pkg_resources.working_set]


def packages_info():
    def parse_meta(meta, k):
        for item in (str(x).split(": ") for x in meta):
            if item[0] == k:
                try:
                    return item[1].strip()
                except IndexError:
                    break
        return "unknown"

    def packages():
        for dist in PACKAGES:
            pkg_dist = pkg_resources.get_distribution(dist)
            meta = list(pkg_dist._get_metadata(pkg_dist.PKG_INFO))
            yield {
                "name": pkg_dist.key,
                "location": pkg_dist.location,
                "version": pkg_dist.version,
                "author": parse_meta(meta, "Author"),
                "author_email": parse_meta(meta, "Author-email"),
                "license": parse_meta(meta, "License"),
                "summary": parse_meta(meta, "Summary"),
                "url": parse_meta(meta, "Home-page"),
            }

    return {
        "lib_path": pkg_resources.WorkingSet().entries,
        "packages": [x for x in packages()]
    }


def _add_level_name(level, name):
    logging._acquireLock()
    try:
        level_name = logging.getLevelName(level)
        logging.addLevelName(level, name)
        if not level_name.startswith("Level"):
            logging.addLevelName(level, level_name)
    finally:
        logging._releaseLock()


TRACE = VERBOSE = 5
ALL = -2 ** 32


def _logger_arg_deser(o):
    if isinstance(o, (Mapping, LambdaContext, Sequence)):
        try:
            return AwsJSONEncoder().encode(o)
        except TypeError:
            pass

    return o


class LambdaLogger(logging.Logger):
    logging.addLevelName(logging.NOTSET, "OFF")
    logging.addLevelName(VERBOSE, "VERBOSE")
    logging.addLevelName(TRACE, "TRACE")
    logging.addLevelName(ALL, "ALL")

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False):
        args = tuple(_logger_arg_deser(arg) for arg in args)

        super()._log(level, msg, args, exc_info=exc_info, extra=extra, stack_info=stack_info)

    def trace(self, message, *args, **kws):
        if self.isEnabledFor(TRACE):
            self._log(TRACE, message, args, **kws)


def lambda_logger(name=None, custom_logger=True, log_level=None, log_format=None,
                  disable_packages_loggers=None, enable_packages_loggers=None):

    name = name or os.getenv("AWS_LAMBDA_FUNCTION_NAME", __name__)
    custom_logger = custom_logger or False
    log_level = log_level or logging.WARNING
    disable_packages_loggers = disable_packages_loggers or False
    enable_packages_loggers = enable_packages_loggers or list()
    log_format = log_format or AWS_LAMBDA_DEFAULT_LOGGING_FORMAT
    log_format = log_format if AWS_LAMBDA_ENVIRONMENT else log_format.replace("%(aws_request_id)s", str(uuid.uuid4()))

    if isinstance(log_level, int):
        level = log_level
    elif isinstance(log_level, str):
        level = logging.getLevelName(log_level)
    else:
        raise TypeError("log_level - expected int or string but got %r " % type(log_level))

    formatter = logging.Formatter(log_format, "%Y-%m-%dT%H:%M:%S")
    formatter.converter = time.gmtime

    # For disable / enable loggers must done before define logger into AWS Environment
    if AWS_LAMBDA_ENVIRONMENT:
        external_loggers = {lg: logging.getLogger(lg) for lg in {*logging.root.manager.loggerDict, *PACKAGES}}
        for ex_name, ex_logger in external_loggers.items():
            enabled = not disable_packages_loggers or any(True for epl in enable_packages_loggers if epl in ex_name)
            if enabled:
                ex_logger.setLevel(level)
                ex_logger.propagate = True
                for h in ex_logger.handlers:
                    h.setFormatter(formatter)
            else:
                ex_logger.setLevel(level)
                ex_logger.propagate = False

    if custom_logger:
        logging.setLoggerClass(LambdaLogger)
    logger = logging.getLogger(name)

    if not AWS_LAMBDA_ENVIRONMENT:
        handler = logging.StreamHandler()
        logger.addHandler(handler)

        for lg in enable_packages_loggers:
            ex_logger = logging.getLogger(lg)
            ex_logger.addHandler(handler)
            ex_logger.setLevel(level)

    for h in logger.handlers:
        h.setFormatter(formatter)

    logger.setLevel(level)

    return logger


def func_logger(logger: logging.Logger = None, display_name: str = None, hide_args: bool = None):
    """Decorates the following function to log values of the input attributes.
        Args:
            logger (:obj:`logging.Logger`): Raw data in csv format (delimiter=',', quote character='"')
            display_name (str) (optional): Name of the function to display
            hide_args (bool): If True do NOT display attributes values (for example, for security reasons)
        Returns:
            decorator
    """
    logger = logger or logging.getLogger(__name__)

    def real_decorator(function):
        f_name = display_name or " ".join(x.capitalize() for x in function.__name__.split("_") if len(x) > 0)

        def wrapper(*args, **kwargs):
            f_id = str(uuid.uuid4())
            logger.debug("Start execution %r, FunctionID: %s", f_name, f_id)

            args_name = inspect.getfullargspec(function).args
            if args_name is not None:
                for ix, item in enumerate(zip(args_name, args)):
                    logger.debug("FunctionID: %s, Positional argument %r: %s", f_id, item[0], item[1])
            for ix, item in enumerate(kwargs.items()):
                logger.debug("FunctionID: %s, Keyword argument %r: %s", f_id, item[0], item[1])

            start_time = time.perf_counter()
            try:
                return function(*args, **kwargs)
            except Exception:
                logger.exception("Fatal error in FunctionID: %s", f_id)
                raise
            finally:
                logger.debug("Complete execution %r, duration %.3f ms, FunctionID: %s",
                             f_name, (time.perf_counter() - start_time) * 1000, f_id)

        return wrapper
    return real_decorator
