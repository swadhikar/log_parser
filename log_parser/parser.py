import os
import time
import re
from dateutil.parser import parse

from elastic.elastic_helper import add_log_info
from log_parser.file_util import reverse_read_files, get_files
from log_parser.models import Config
from common import convert_time_format, get_dummy_time


# Todo: Need to move Log into different file
class Log:
    def __init__(self, line, message_format, dummy=False):
        self.timestamp = None
        self.level = None
        self.message = None
        self.message_format = message_format
        self.text = line
        self.parse_line(line, dummy)

    def parse_line(self, line, dummy):
        if dummy:
            self.timestamp = get_dummy_time()
            self.level = ''
            self.message = ''
        else:
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
        self.last_log_line = Log('', self.message_format, dummy=True)

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
                    add_log_info(
                        index='log_info',  # todo: Need to move index to config
                        timestamp=current_log.timestamp,
                        level=current_log.level,
                        message=current_log.message,
                        app_name=self.config.app_name
                    )
                else:
                    break

            if first_read_line.strip() != '':  # bug
                self.last_log_line = Log(first_read_line, self.message_format)

        except Exception as e:
            print(f'Failed to store log info into ES: {e}')

    def start_poll(self):
        polling_interval = self.config.poll_interval
        print(f'Started polling against log for app: {self.config.app_name} for '
              f'every "{polling_interval}" seconds')

        while True:
            self.poll_logs()
            time.sleep(polling_interval)

    def __repr__(self):
        return f'Applog<{self.config.app_name}>'


if __name__ == '__main__':
    from constants import APP_CONFIG
    from log_parser.file_util import read_json_config, pretty_print

    # Read json config as dictionary
    # config_json = read_json_config(APP_CONFIG)[0]
    config_json = read_json_config(APP_CONFIG)[1]

    # Create configuration object
    _config = Config(**config_json)

    # Create AppLog object
    app_log = AppLog(_config)
    app_log.start_poll()
