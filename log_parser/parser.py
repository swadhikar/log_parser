import os
import time

from datetime import datetime
from log_parser.file_util import read_json_config, reverse_read_files, get_files
from constants import dummy_line, APP_CONFIG
from multiprocessing import Process
from log_parser.models import Config

app_config_list = []


def load_app_config(return_apps=False):
    global app_config_list
    app_info_list = read_json_config(APP_CONFIG)

    if return_apps and app_info_list:
        return app_config_list

    for app_info in app_info_list:
        config = Config(**app_info)
        app_config_list.append(config)

    print(f'Found "{len(app_config_list)}" app_config_list to be monitored ...')
    if return_apps:
        return app_config_list


class Log:
    def __init__(self, line):
        self.timestamp = None
        self.message = None
        self.text = line
        self.parse_line(line)

    def parse_line(self, line, timestamp_format='%m/%d/%Y %H:%M:%S.%f'):
        date_str = line[:23]
        if date_str:
            self.timestamp = datetime.strptime(date_str, timestamp_format)
            self.message = line[23:].rstrip()

    def __repr__(self):
        return f'{self.text[:30]} ...'


class AppLog:

    def __init__(self, config):
        self.config = config
        self.last_log_line = Log(dummy_line)

    def poll_logs(self):
        """
            Polls apps log on an interval configured
                until last polled time is reached reverse_read file
        """
        file_path = os.path.dirname(self.config.app_log)
        files = get_files(file_path)

        first_read_line = ''

        try:
            for index, line in enumerate(reverse_read_files(files)):
                current_log = Log(line)
                if index == 0:
                    first_read_line = line
                if current_log.timestamp > self.last_log_line.timestamp:
                    print(line, end='')  # process failure point lines (store to es)
                    # process_app(self.config.app_name)
                else:
                    break

                if first_read_line.strip() != '':  # bug
                    self.last_log_line = Log(first_read_line)
        except:
            print('Failure happened...')

    def start_poll(self):
        polling_interval = self.config.poll_interval
        print(f'Started polling against log for app: {self.config.app_name} for '
              f'every "{polling_interval}" seconds')

        while True:
            self.poll_logs()
            time.sleep(polling_interval)


if __name__ == '__main__':
    _config = load_app_config(return_apps=True)
    process_list = []

    for app_config in _config:
        _process = Process(target=AppLog(app_config).start_poll, name=app_config.app_name)
        _process.start()
        print(f'Started monitor app "{app_config.app_name}" in process: {_process.name}')
        process_list.append(_process)

    # print(config)

    app_log = AppLog(_config)
    app_log.start_poll()

    import csv
