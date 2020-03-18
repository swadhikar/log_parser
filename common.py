import json


def pretty_print(iterable, indent=1):
    indented_text = json.dumps(iterable, indent=indent)
    print(indented_text)
