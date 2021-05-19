import pytest
import errors
import os
import utils


def test_get_dict_from_yaml():
    yaml_string = """
        a: 1
        b:
            c: 3
            d: 4
    """
    expected_dict = {
        'a': 1,
        'b': {'c': 3, 'd': 4}
    }
    dictionary = utils.get_dict_from_yaml(yaml_string)
    assert dictionary == expected_dict


def test_get_dict_yaml_raises_invalid_input_error():
    with pytest.raises(errors.InvalidInputException):
        utils.get_dict_from_yaml('invalid}')


def test_load_config(tmpdir, monkeypatch):
    yaml_string = """
        a: 1
        b: 2
    """
    yaml_file = tmpdir.mkdir("sub").join("test.yaml")
    yaml_file.write(yaml_string)

    def mock_get_config_file_name():
        return yaml_file.strpath
    monkeypatch.setattr(utils, 'get_config_file_name', mock_get_config_file_name)
    dictionary = utils.load_config_file()
    assert dictionary == {'a': 1, 'b': 2}


def test_load_config_file_error(monkeypatch):
    def mock_get_config_file_name():
        return 'invalid_path'
    monkeypatch.setattr(utils, 'get_config_file_name', mock_get_config_file_name)
    with pytest.raises(FileNotFoundError):
        dictionary = utils.load_config_file()


def test_get_config_file_name(monkeypatch):
    def mock_get_env_prod(name, default):
        return 'prod'

    def mock_get_env_dev(name, default):
        return 'dev'

    def mock_get_env_invalid(name, default):
        return ''

    with monkeypatch.context() as m:
        m.setattr(os, 'getenv', mock_get_env_prod)
        assert utils.get_config_file_name() == 'app.yaml'

        m.setattr(os, 'getenv', mock_get_env_dev)
        assert utils.get_config_file_name() == 'app_dev.yaml'

        m.setattr(os, 'getenv', mock_get_env_invalid)
        assert utils.get_config_file_name() == 'app_dev.yaml'
