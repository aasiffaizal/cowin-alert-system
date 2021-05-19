import errors
import yaml
import os


def get_config_file_name():
    return 'app.yaml' if os.getenv('ENV', None) == 'prod' else 'app_dev.yaml'


def get_dict_from_yaml(yaml_str: str) -> dict:
    try:
        retrieved_dict = yaml.safe_load(yaml_str)
        assert isinstance(retrieved_dict, dict)
        return retrieved_dict
    except (AssertionError, yaml.YAMLError) as e:
        raise errors.InvalidInputException(e)


def load_config_file():
    # will elaborate when more config files are added.
    # For now one only one config and one environment.
    yaml_file = get_config_file_name()
    with open(yaml_file) as f:
        file_contents = f.read()
        f.close()
        return get_dict_from_yaml(file_contents)
