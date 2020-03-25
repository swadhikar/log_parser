import os
import json
from constants import LOG_DIR, APP_CONFIG
from common import pretty_print
from multiprocessing import Lock

lock = Lock()


def reverse_read_files(file_list):
    """Generator function"""
    # TODO: Need to include logging
    for filename in file_list:
        file = open(filename)
        print(f'Reading "{os.path.basename(filename)}" reversed...')
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


def read_json_config(config_path):
    with open(config_path) as json_file:
        data = json.load(json_file)
    return data


def get_files(file_path):
    listed_files = os.listdir(file_path)
    print(listed_files)
    files_list = [os.path.join(file_path, file) for file in listed_files[1:]]
    print(f'Before sorting: {files_list}')
    rotated_files = sorted(files_list, reverse=True)
    print(f'After sorting: {rotated_files}')
    return [os.path.join(file_path, listed_files[0])] + rotated_files
"""
# pseudocode:
# get all the files in applog dir
listed_files = os.listdir(file_path)
# form full path for the files
# skip webapp.log and 
files_list = [os.path.join(file_path, file) for file in listed_files[1:]]
# reverse sort all other files
sorted(files_list, reverse=True)
# append webapp.log and reversed file names
[os.path.join(file_path, listed_files[0])] + rotated_files
"""

if __name__ == '__main__':
    # from log_parser.models import Config
    #
    # d = read_json_config(APP_CONFIG)
    # pretty_print(d)
    # for i in d:
    #     pretty_print(i)
    #     config = Config(**i)

    files = get_files(r'C:\Users\schandramohan\Documents\swadhi\test_git\log_parser\logs\web_app')
    pretty_print(files)

    # logs = get_log_files_for_app('web_app_2')
    # pretty_print(logs)
