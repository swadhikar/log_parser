import json


def pretty_print(iterable, indent=1):
    indented_text = json.dumps(iterable, indent=indent)
    print(indented_text)


def str_to_dict(string):
    result = eval(f'{string}')
    return result


if __name__ == '__main__':
    d = {
        "app_name": "web_app", "log_file": "webapp.log",
        "log_path": "C:\\Users\\schandramohan\\Documents\\swadhi\\test_git\\trial_and_error\\logs", "poll_interval": 1,
        "server_ip": "127.0.0.1", "server_port": 3010
    }

    pretty_print(d, indent=4)
