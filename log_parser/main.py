from log_parser.models import Config
from log_parser.file_util import read_json_config, pretty_print
from constants import APP_CONFIG
from multiprocessing import Process
from log_parser.parser import ParserFactory

app_config_list = []


def load_app_config():
    app_info_list = read_json_config(APP_CONFIG)

    global app_config_list

    for app_info in app_info_list:
        config = Config(**app_info)
        app_config_list.append(config)

    print(f'Found "{len(app_config_list)}" app_config_list to be monitored ...')

    LOG_MONITOR_THREADS = []

    # Create processs
    for app in app_config_list:
        parser = ParserFactory.get_instance_for_app(app)
        process = Process(target=parser.poll, name=app.app_name)
        LOG_MONITOR_THREADS.append(process)

    # Start polling
    for process in LOG_MONITOR_THREADS:
        process.start()
        print(f'Started monitoring process: {process.name}')


if __name__ == '__main__':
    load_app_config()
