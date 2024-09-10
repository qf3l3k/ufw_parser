import logging
import yaml


logger = logging.getLogger("ufw_parser_log")


def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)
