import time
import random
from datetime import datetime
from log_parser.parser import ParserFactory
from log_parser.models import Config
from log_parser.file_util import read_json_config, pretty_print
from constants import APP_CONFIG

test_log_file = '../tests/logfile.log'
test_log_lines = ('Welcome to python programming ...',
                  'Java is being overtaken by python!',
                  'Successfully deployed app. Restarting server ...',
                  'Server restart successful. Waiting for apps to be up ...',
                  '5!=3, values mismatch :(')


def load_logs(filename, num_lines=1):
    timestamp_format = '%m/%d/%Y %H:%M:%S.%f'
    print(f'Dumping {num_lines} line to the test log: {filename}...')

    # Generate log
    lines = []
    for _ in range(num_lines):
        current_time = datetime.now().strftime(timestamp_format)[:-3]
        lines.append(f'{current_time}: {random.choice(test_log_lines)}\n')

    if lines:
        with open(filename, 'a') as _file:
            _file.writelines(lines)

    time.sleep(1)


def test_parser():
    parser = ParserFactory.get_instance_for_app(test_log_file)

    for num in [1, 3, 2, 0, 0, 1]:
        lines = [line for line in parser.poll_log() if line]
        print(f'Detected {len(lines)} new lines!')
        parser.dump_logs(num, test_log_lines=test_log_lines)


def test_has_log_rolled():
    parser = ParserFactory.get_instance_for_app(test_log_file)
    for _ in parser.poll_log(): pass
    has_logged = parser.has_log_rolled()
    assert not has_logged, "Log shouldn't have rolled"

    for _ in parser.poll_log(): pass
    parser.dump_logs(num_lines=1)
    has_logged = parser.has_log_rolled()
    assert has_logged, "Log should have rolled"

    for _ in parser.poll_log(): pass
    parser.dump_logs(num_lines=0)
    has_logged = parser.has_log_rolled()
    print(f'has_logged: {has_logged}')
    assert not has_logged, "Log shouldn't have rolled"


def test_poll_log():
    d = read_json_config(APP_CONFIG)
    for i in d:
        pretty_print(i)
        config = Config(**i)
        parser = ParserFactory.get_instance_for_app(config)


def dump_logs(app_name):
    d = read_json_config(APP_CONFIG)
    for i in d:
        if i.get('app_name') == app_name:
            config = Config(**i)
            parser = ParserFactory.get_instance_for_app(config)
            for _ in range(15):
                parser.dump_logs(100, test_log_lines=test_log_lines)
                print("Dumped logs!")
                time.sleep(10)


if __name__ == '__main__':
    dump_logs('web_app')
    # test_parser()
    # test_has_log_rolled()
    # test_poll_log()
