import json


def pretty_print(iterable, indent=1):
    indented_text = json.dumps(iterable, indent=indent)
    print(indented_text)


def str_to_dict(string):
    result = eval(f'{string}')
    return result


def convert_time_format(format):
    new_format = format.replace('[', '\[') \
        .replace(']', '\]') \
        .replace('timestamp', '(.*)') \
        .replace('level', '(.*?)') \
        .replace('message', '(.*)')
    print(f'Date format converted: {new_format}')
    return new_format


def get_dummy_line(time_format):
    from datetime import datetime
    past_date = datetime(day=1, month=1, year=1900, hour=0, minute=0, second=0)
    text = past_date.strptime(past_date, time_format)
    print(text)

# convert_time_format('[timestamp Europe/Paris] level: message')
# convert_time_format('timestamp - level: message')
