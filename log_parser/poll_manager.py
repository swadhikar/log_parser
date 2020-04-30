from log_parser.parser import AppLog
from log_parser.models import Config
from multiprocessing import Process
import time

import constants
from log_parser.file_util import read_json_config


class PollManager:
    """
        Manages all poll related tasks.

        1. Schedules polling task in parallel
        2. Looks for rotated log files and updates the object
        3. Provide APIs to kill/restart polling operation
    """
    POLL_JOB_DB = {}

    def __init__(self):
        self._start_scheduler()

    @staticmethod
    def _parse_config():
        # Read config file and fetch list of apps
        config_list = read_json_config(constants.APP_CONFIG)

        # Create instances
        for config in config_list:
            # Skip those apps which where already processed
            if config['app_name'] in PollManager.POLL_JOB_DB:
                continue

            config_obj = Config(**config)

            print(f'Detected new app for polling: {config_obj.app_name}')
            PollManager.POLL_JOB_DB[config_obj.app_name] = {
                'app_log': AppLog(config_obj),
                'status': constants.SCHEDULED
            }

    @classmethod
    def _create_process(cls, app_name, app_log_instance):
        process = Process(target=app_log_instance.start_poll, name=app_name)
        process.start()
        PollManager.POLL_JOB_DB[app_name]['status'] = constants.STARTED  # update status
        print(f'Started monitoring process for app: {app_name}')

    @classmethod
    def _schedule_jobs(cls):
        for app_name, app_info_dict in PollManager.POLL_JOB_DB.items():
            # Filter scheduled jobs
            if app_info_dict['status'] != constants.SCHEDULED:
                continue

            # Create a process that polls this app
            cls._create_process(app_name, app_log_instance=app_info_dict['app_log'])

    @classmethod
    def _start_scheduler(cls, config_read_interval=5 * 1):
        while True:
            # Read json to find new jobs
            cls._parse_config()

            # Start scheduling the new jobs
            cls._schedule_jobs()
            # print(f'{PollManager.POLL_JOB_DB}')

            # Wait and read
            time.sleep(config_read_interval)


if __name__ == '__main__':
    PollManager()
