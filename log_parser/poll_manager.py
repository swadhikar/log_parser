from log_parser.parser import AppLog
from log_parser.models import Config
from multiprocessing import Process

from constants import APP_CONFIG
from log_parser.file_util import read_json_config, pretty_print


class PollManager:
    """
        Manages all poll related tasks.

        1. Schedules polling task in parallel
        2. Looks for rotated log files and updates the object
        3. Provide APIs to kill/restart polling operation
    """
    POLL_JOB_DB = {}

    def __init__(self, config):
        self.config = config
        self._parse_config(config)
        self._start_scheduler()

    @staticmethod
    def _parse_config(config_list):
        # Create instances
        for config in config_list:
            config_obj = Config(**config)
            parser = AppLog(config_obj)
            PollManager.POLL_JOB_DB[config_obj.app_name] = parser

    @classmethod
    def _start_scheduler(cls):
        for app_name, parser in PollManager.POLL_JOB_DB.items():
            process = Process(target=parser.start_poll, name=app_name)
            process.start()
            print(f'Started monitoring process: {process.name}')


def main():
    """Start of execution"""
    config_data = read_json_config(APP_CONFIG)
    pretty_print(config_data)
    PollManager(config_data)


if __name__ == '__main__':
    main()
