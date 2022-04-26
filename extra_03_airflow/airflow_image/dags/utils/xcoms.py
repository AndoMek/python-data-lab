from functools import wraps
from typing import Callable


def is_jinja_template(func: Callable):
    """ Decorator for convert xcom string to jinja template

    For most cases it's useful to get {{ taplate_string }}
    But for some cases we integrate xcom into template in this case
    we don't need to trailing string with curly brackets

    Args:
        func: function to decorate
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        """ Function Wrapper

        Args:
            *args: function arguments
            **kwargs: function keywords

        If keyword `is_template` set to True or not exist than trail sting with
        curly brackets otherwise return string without modification
        """
        is_template = kwargs.get("is_template", "True")
        if is_template:
            return "{{ %s }}" % func(*args, **kwargs)
        else:
            return func(*args, **kwargs)

    return wrapper


@is_jinja_template
def xcom_pull(task_id, key="return_value", **kwargs):
    """ Jinja2 template xcom_pull

    Args:
        task_id: a unique, meaningful id for the task
        key: xcom key. By default uses "return_value" if set to None than return all keys

    If keyword `is_template` set to True or not exist than trail sting with
        curly brackets otherwise return string without modification

    Examples:
        >>> xcom_pull("sample")
        "{{ task_instance.xcom_pull('sample', key='return_value') }}"
        >>> xcom_pull("sample", key="another_value")
        "{{ task_instance.xcom_pull('sample', key='another_value') }}"
        >>> xcom_pull("sample", key="another_value", is_template=False)
        "task_instance.xcom_pull('sample', key='another_value')"

    Returns:
        Jinja2 template with access to xcom
    """
    xcom = "task_instance.xcom_pull('%s', key='%s')" % (task_id, key)
    return xcom


@is_jinja_template
def xcom_pull_map(task_id: str, map_path: str, key: str = "return_value", **kwargs):
    """ Jinja2 template xcom_pull with access to key in python dictionary

    Args:
        task_id: a unique, meaningful id for the task
        map_path: specify path to map with dot notation
        key: xcom key. By default uses "return_value" if set to None than return all keys

    map_path converted to python key access, eg:
        key1 -> ['key1']
        key1.key2 -> ['key1']['key2']
        key1.key2.key3 -> ['key1']['key2'][key3]

    If keyword `is_template` set to True or not exist than trail sting with
        curly brackets otherwise return string without modification

    Examples:
        >>> xcom_pull_map("sample", "key1.key2")
        "{{ task_instance.xcom_pull('sample', key='return_value')['key1']['key2'] }}"
        >>> xcom_pull_map("sample", "")
        "{{ task_instance.xcom_pull('sample', key='return_value') }}"
        >>> xcom_pull_map("sample", "key1.key2", key="another_value")
        "{{ task_instance.xcom_pull('sample', key='another_value')['key1']['key2'] }}"
        >>> xcom_pull_map("sample", "key1.key2", key="another_value", is_template=False)
        "task_instance.xcom_pull('sample', key='another_value')['key1']['key2']"

    Returns:
        Jinja2 template with access to xcom
    """
    if not map_path:
        return xcom_pull(task_id=task_id, key=key, is_template=False)

    python_dict_path = "".join("['%s']" % item for item in map_path.split("."))
    return xcom_pull(task_id=task_id, key=key, is_template=False) + python_dict_path


@is_jinja_template
def xcom_pull_list(task_id: str, ix: int, key: str = "return_value", **kwargs):
    """ Jinja2 template xcom_pull with access to index in python list/tuple

    Args:
        task_id: a unique, meaningful id for the task
        ix: list/tuple index
        key: xcom key. By default uses "return_value" if set to None than return all keys

    ix to python list index access, eg:
        0 -> [0]
        -1 -> [-1]

    If keyword `is_template` set to True or not exist than trail sting with
        curly brackets otherwise return string without modification

    Examples:
        >>> xcom_pull_list("sample", 0)
        "{{ task_instance.xcom_pull('sample', key='return_value')[0] }}"
        >>> xcom_pull_list("sample", -1, key="another_value")
        "{{ task_instance.xcom_pull('sample', key='another_value')[-1] }}"
        >>> xcom_pull_list("sample", 42, key="another_value", is_template=False)
        "task_instance.xcom_pull('sample', key='another_value')[42]"

    Returns:
        Jinja2 template with access to xcom
    """
    return "%s[%s]" % (xcom_pull(task_id=task_id, key=key, is_template=False), ix)
