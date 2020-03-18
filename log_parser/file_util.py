import os
import json
from constants import LOG_DIR, APP_CONFIG
from common import pretty_print
from multiprocessing import Lock

lock = Lock()


def reverse_read(filename):
    """Generate the lines of file in reverse order"""
    file = open(filename)
    try:
        lock.acquire()
        part = ''
        for block in _reversed_blocks(file):
            for char in reversed(block):
                if char == '\n' and part.strip():
                    yield part[::-1]
                    part = ''
                part += char
        if part.strip():
            yield part[::-1]
    finally:
        file.close()
        lock.release()


def _reversed_blocks(file, block_size=4096):
    """Generate blocks of file's contents in reverse order"""
    file.seek(0, os.SEEK_END)
    here = file.tell()
    while 0 < here:
        delta = min(block_size, here)
        here -= delta
        file.seek(here, os.SEEK_SET)
        yield file.read(delta)


def get_log_files(path, extension='.log'):
    print(f'Fetching logs from path: {path}')

    if not os.path.exists(path):
        raise FileNotFoundError(f'Unable to find path: {path}')

    files = [
        _file
        for _file in os.listdir(path)
        if os.path.isfile(f'{path}/{_file}') and _file.endswith(extension)
    ]

    return files


def get_log_files_for_app(app_name):
    app_log_path = os.path.join(LOG_DIR, app_name)
    log_files = []

    try:
        log_files = get_log_files(app_log_path)
    except FileNotFoundError as e:
        print(f'Unable to find logs for app "{app_name}". Exception trace: {e}')

    return log_files


def read_json_config(config_path):
    with open(config_path) as json_file:
        data = json.load(json_file)
    return data


if __name__ == '__main__':
    from log_parser.models import Config
    d = read_json_config(APP_CONFIG)
    pretty_print(d)
    for i in d:
        pretty_print(i)
        config = Config(**i)

    # get_log_files(LOG_DIR)
    # logs = get_log_files_for_app('web_app')
    # pretty_print(logs)
    #
    # logs = get_log_files_for_app('web_app_2')
    # pretty_print(logs)
