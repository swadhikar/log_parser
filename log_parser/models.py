from dataclasses import dataclass
import os


@dataclass
class Config:
    app_name: str
    log_file: str
    log_path: str
    poll_interval: int
    server_ip: str
    server_port: int

    def __post_init__(self):
        self.app_log = os.path.join(self.log_path, self.app_name, self.log_file)
