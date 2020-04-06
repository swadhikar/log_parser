import json


def pretty_print(iterable, indent=1):
    indented_text = json.dumps(iterable, indent=indent)
    print(indented_text)


def str_to_dict(string):
    result = eval(f'{string}')
    return result
