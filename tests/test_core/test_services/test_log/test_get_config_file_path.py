import os

import pytest
import tempfile

from waster.core.services.log import _get_config_file_path, LOGGING_CFG_ENVVAR, LOGGING_CFG_DEFAULT  # NOQA


def test_get_config_file_path___w_file_wo_envvar():
    # With a file but no environment variable
    temp = tempfile.TemporaryFile()
    result = _get_config_file_path(temp.name)
    assert result == temp.name


def test_get_config_file_path___w_file_w_envvar():
    # With environment variable and a file
    os.environ[LOGGING_CFG_ENVVAR] = 'foo.json'
    temp = tempfile.TemporaryFile()
    result = _get_config_file_path(temp.name)
    assert result == temp.name


def test_get_config_file_path___wo_file_w_envvar():
    # With environment variable but without file
    temp = tempfile.TemporaryFile()
    print(f'TEMP NAME: {temp.name}')
    os.environ[LOGGING_CFG_ENVVAR] = temp.name
    result = _get_config_file_path()
    assert result == temp.name


def test_get_config_file_path___bad_file():
    # Provided file does not exist
    with pytest.raises(FileNotFoundError):
        _get_config_file_path('foo.json')


def test_get_config_file_path___bad_envvar():
    # Environment variable file does not exist
    os.environ[LOGGING_CFG_ENVVAR] = 'foo.json'
    with pytest.raises(FileNotFoundError):
        _get_config_file_path()


def test_get_config_file_path___default():
    # No file and no environment variable
    os.environ.pop(LOGGING_CFG_ENVVAR)
    if not os.path.isdir(os.path.dirname(LOGGING_CFG_DEFAULT)):
        os.mkdir(os.path.dirname(LOGGING_CFG_DEFAULT))

    with open(LOGGING_CFG_DEFAULT, 'w') as file:
        file.write('{}')

        result = _get_config_file_path()
        assert result == LOGGING_CFG_DEFAULT

    os.remove(LOGGING_CFG_DEFAULT)
    os.rmdir(os.path.dirname(LOGGING_CFG_DEFAULT))
