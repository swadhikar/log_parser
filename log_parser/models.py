from dataclasses import dataclass
import os
from constants import LOG_DIR


@dataclass
class Config:
    app_name: str
    message_format: str
    log_file: str
    poll_interval: int

    def __post_init__(self):
        self.app_log = os.path.join(LOG_DIR, self.app_name, self.log_file)


if __name__ == '__main__':
    from constants import APP_CONFIG
    from log_parser.file_util import read_json_config, pretty_print

    config_data = read_json_config(APP_CONFIG)[0]

    config = Config(**config_data)
    print(config)

