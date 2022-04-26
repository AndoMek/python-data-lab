import os
import yaml
import json


def get_dag_config(dag_filepath, config_type="yaml"):
    root = os.path.dirname(dag_filepath)
    basename, _ = os.path.basename(dag_filepath).split(".", 1)
    config_type = config_type.lower()

    if config_type == "yaml":
        with open(os.path.join(root, "configs", basename + ".yml"), "r") as fp:
            config = yaml.safe_load(fp)
    elif config_type == "json":
        with open(os.path.join(root, "configs", basename + ".json"), "r") as fp:
            config = json.load(fp)

    return config
