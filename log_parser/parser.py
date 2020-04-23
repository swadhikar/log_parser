import os
import time
import re
from dateutil.parser import parse

from elastic.elastic_helper import add_log_info
from log_parser.file_util import read_json_config, reverse_read_files, get_files, reverse_read
from constants import dummy_line
from log_parser.models import Config
from common import convert_time_format

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
    def __init__(self, line, message_format):
        self.timestamp = None
        self.level = None
        self.message = None
        self.message_format = message_format
        self.text = line
        self.parse_line(line)

    def parse_line(self, line):
        search_object = re.search(self.message_format, line)
        date_str = search_object.group(1)
        self.timestamp = parse(date_str)
        self.level = search_object.group(2)
        self.message = search_object.group(3)

    def __repr__(self):
        return f'Log<{self.timestamp} - {self.level}: {self.message[:20]}> ...'


class AppLog:

    def __init__(self, config):
        self.config = config
        self.message_format = convert_time_format(config.message_format)
        self.last_log_line = Log(dummy_line, self.message_format)

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
                current_log = Log(line, self.message_format)

                if index == 0:
                    first_read_line = line

                if current_log.timestamp > self.last_log_line.timestamp:
                    # print(current_log.timestamp, end=' ' * 10)  # process failure point lines (store to es)
                    # print(current_log.level, end=' ' * 10)  # process failure point lines (store to es)
                    # print(current_log.message[:50])  # process failure point lines (store to es)
                    #
                    add_log_info(
                        index='log_info',
                        timestamp=current_log.timestamp,
                        level=current_log.level,
                        message=current_log.message,
                        app_name=config.app_name
                    )
                else:
                    break

            if first_read_line.strip() != '':  # bug
                self.last_log_line = Log(first_read_line, self.message_format)

        except Exception as e:
            print(f'Failure happened...: {e}')

    def start_poll(self):
        polling_interval = self.config.poll_interval
        print(f'Started polling against log for app: {self.config.app_name} for '
              f'every "{polling_interval}" seconds')

        while True:
            self.poll_logs()
            time.sleep(polling_interval)


if __name__ == '__main__':
    from constants import APP_CONFIG
    from log_parser.file_util import read_json_config, pretty_print

    # Read json config as dictionary
    config_json = read_json_config(APP_CONFIG)[0]

    # Create configuration object
    config = Config(**config_json)

    # Create AppLog object
    app_log = AppLog(config)
    app_log.start_poll()
