from typing import List

import jsonpickle
import os
import os.path

from config import Configuration, default_configuration
from instances import Site

base_path = os.path.join(os.getenv("HOME"), ".cloudsql")
instance_filename = os.path.join(base_path, "instances.json")
config_filename =  os.path.join(base_path, "config.json")


def save_site(site : Site):
    if not os.path.exists(os.path.dirname(instance_filename)):
        os.makedirs(os.path.dirname(instance_filename))

    with open(instance_filename, 'w') as f:
        f.write(jsonpickle.encode(site))


def load_site() -> Site:
    if not os.path.exists(instance_filename):
        return Site({})
    else:
        with open(instance_filename, 'r') as f:
            json_str = f.read()
            return jsonpickle.decode(json_str)


def save_config(config: Configuration):
    if not os.path.exists(os.path.dirname(config_filename)):
        os.makedirs(os.path.dirname(config_filename))

    with open(config_filename, 'w') as f:
        f.write(jsonpickle.encode(config))


def load_config() -> Configuration:
    if not os.path.exists(config_filename):
        return default_configuration()
    else:
        with open(config_filename, 'r') as f:
            json_str = f.read()
            return jsonpickle.decode(json_str)