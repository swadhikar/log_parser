import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(PROJECT_DIR, 'logs')
APP_CONFIG = os.path.join(PROJECT_DIR, 'config', 'app.json')

print(APP_CONFIG)

# print(f'Project dir : {PROJECT_DIR}')
# print(f'Log path    : {LOG_DIR}')

dummy_line = '01/01/1900 00:00:00.000: Just a dummy line'
