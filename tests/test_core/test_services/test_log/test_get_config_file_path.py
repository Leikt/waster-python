import os

import pytest

from waster.core.services.log import _get_config_file_path, LOGGING_CFG_ENVVAR, LOGGING_CFG_DEFAULT  # NOQA


def _create_temp_file(filename: str) -> str:
    path = f'./{filename}'
    with open(path, 'w') as file:
        file.write('{}')

    return path


def _init():
    if LOGGING_CFG_ENVVAR in os.environ:
        os.environ.pop(LOGGING_CFG_ENVVAR)


def test_get_config_file_path___w_file_wo_envvar():
    # With a file but no environment variable
    _init()
    path = _create_temp_file('test_get_config_file_path___w_file_wo_envvar.json')
    assert _get_config_file_path(path) == path


def test_get_config_file_path___w_file_w_envvar():
    # With environment variable and a file
    _init()
    path = _create_temp_file('test_get_config_file_path___w_file_w_envvar.json')
    os.environ[LOGGING_CFG_ENVVAR] = 'foo.json'
    assert _get_config_file_path(path) == path


def test_get_config_file_path___wo_file_w_envvar():
    # With environment variable but without file
    _init()
    path = _create_temp_file('test_get_config_file_path___wo_file_w_envvar.json')
    os.environ[LOGGING_CFG_ENVVAR] = path
    assert _get_config_file_path() == path


def test_get_config_file_path___bad_file():
    # Provided file does not exist
    _init()
    with pytest.raises(FileNotFoundError):
        _get_config_file_path('foo.json')


def test_get_config_file_path___default():
    # No file and no environment variable
    _init()
    if not os.path.isdir('config'):
        os.mkdir('config')
    if not os.path.isfile('config/logging.json'):
        with open('config/logging.json', 'w') as file:
            file.write('{}')

    assert _get_config_file_path() == LOGGING_CFG_DEFAULT


def test_get_config_file_path___bad_envvar():
    # Environment variable file does not exist
    _init()
    os.environ[LOGGING_CFG_ENVVAR] = 'foo.json'
    with pytest.raises(FileNotFoundError):
        _get_config_file_path()
