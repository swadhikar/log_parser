from dataclasses import dataclass
import os
from constants import LOG_DIR


@dataclass
class Config:
    app_name: str
    log_file: str
    poll_interval: int
    server_ip: str
    server_port: int

    def __post_init__(self):
        self.app_log = os.path.join(LOG_DIR, self.app_name, self.log_file)


if __name__ == '__main__':
    d = {
        "app_name": "web_app",
        "log_file": "webapp.log",
        "log_path": "C:\\Users\\schandramohan\\Documents\\swadhi\\test_git\\trial_and_error\\logs",
        "poll_interval": 1,
        "server_ip": "127.0.0.1",
        "server_port": 3010
    }

    # print(d.get('log_path') + '/' + d.get('app_name') + '/' + d.get('log_file') )
    config = Config(**d)
    print(config.app_name)
    print(config.poll_interval)
    print(config.app_log)
