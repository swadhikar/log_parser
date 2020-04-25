import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(PROJECT_DIR, 'logs')
APP_CONFIG = os.path.join(PROJECT_DIR, 'config', 'app.json')

# Kibana date time format
KIBANA_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'  # %m/%d/%Y %H:%M:%S.%f

# Dummy line
dummy_line = '[Fri Jan 01 00:00:00.000000 1900 Europe/Paris] info: Just a dummy line'
