import os
import time
import random

from datetime import datetime
from log_parser.file_util import reverse_read

from multiprocessing import Lock

lock = Lock()


class LogLine:
    def __init__(self, line):
        self.timestamp = None
        self.message = None
        self.text = line
        self.parse_line(line)

    def parse_line(self, line, timestamp_format='%m/%d/%Y %H:%M:%S.%f'):
        date_str = line[:23]
        if date_str:
            self.timestamp = datetime.strptime(date_str, timestamp_format)
            self.message = line[23:]

    def __repr__(self):
        return f'Date: {self.timestamp}, Message: {self.message[:15]} ...'


class ParserFactory:
    PARSERS = {}

    @classmethod
    def get_instance_for_app(cls, config):
        if ParserFactory.PARSERS.get(config.app_name):
            return ParserFactory.PARSERS[config.app_name]
        parser_instance = LogFileParser(config)
        ParserFactory.PARSERS[config.app_name] = parser_instance
        return parser_instance


class LogFileParser:
    LOG_DB = {}

    def __init__(self, config):
        self.log_file = config.app_log
        self.config = config
        self.last_log_line = None
        self.prev_poll_time = None
        self.last_file_size = None

    def poll_log(self):
        reversed_file = reverse_read(self.log_file)

        # Capture the last line to be stored for next iteration
        last_line = next(reversed_file)

        if self.has_log_rolled():
            yield last_line

            # Return all lines if not polled before
            if self.prev_poll_time is None:
                for line in reversed_file:
                    yield line
            else:
                for current_line in reversed_file:
                    if LogLine(current_line).timestamp > self.last_log_line.timestamp:
                        yield current_line

        # Set the last logged line after processing
        self.last_log_line = LogLine(last_line)

        # Clear dict and Update last polled time
        self.prev_poll_time = datetime.now()
        LogFileParser.LOG_DB.clear()
        LogFileParser.LOG_DB[self.prev_poll_time] = os.stat(self.log_file).st_size

    def has_log_rolled(self):
        current_file_size = os.stat(self.log_file).st_size
        previous_file_size = LogFileParser.LOG_DB.get(self.prev_poll_time)
        # print(f'{self.config.app_name} - Previous size: {previous_file_size}')
        # print(f'{self.config.app_name} - Current  size: {current_file_size}')

        if previous_file_size is None:  # first time parsing
            return True

        if current_file_size > LogFileParser.LOG_DB.get(self.prev_poll_time):
            return True

        return False

    def dump_logs(self, num_lines=0, test_log_lines=('test 1', 'test2')):
        from multiprocessing import Lock
        lock = Lock()
        timestamp_format = '%m/%d/%Y %H:%M:%S.%f'
        print(f'Dumping {num_lines} line to the test log...')

        # Generate log
        lines = []
        for _ in range(num_lines):
            current_time = datetime.now().strftime(timestamp_format)[:-3]
            lines.append(f'{current_time}: {random.choice(test_log_lines)}\n')

        if lines:
            lock.acquire()
            with open(self.log_file, 'a') as _file:
                _file.writelines(lines)
            lock.release()
        self.last_file_size = os.stat(self.log_file).st_size
        time.sleep(1)

    def poll(self):
        polling_interval = self.config.poll_interval
        print(f'Started polling against log for app: {self.config.app_name}')
        while True:
            lines = [line for line in self.poll_log() if line]
            print(f'Detected {len(lines)} new lines in log: {self.config.app_name}')
            time.sleep(polling_interval)
