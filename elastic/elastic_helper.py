from subprocess import Popen, PIPE
import re

from common import str_to_dict
import constants

import requests

# elastic_host = 'localhost'
# elastic_port = 9200
# elastic_port = 9200
# elastic_url_ = f'{elastic_host}:{elastic_port}'


elastic_url_ = f'https://search-comm-air-metrics-6bn4elbf3jwzp3xk4kdppn2ige.us-east-2.es.amazonaws.com'


# kibana_url = 'https://search-comm-air-metrics-6bn4elbf3jwzp3xk4kdppn2ige.us-east-2.es.amazonaws.com/_plugin/kibana/app'

def execute_command(command):
    result = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    result, error = result.communicate()
    return result.decode('utf-8'), error.decode('utf-8')


def create_index(index):
    query = f'curl -X PUT "{elastic_url_}/{index}"'
    result, error = execute_command(query)
    if re.search('acknowledged.*true', result):
        print(f'Created index successfully: {index}')
        return True
    print(f'Failed to create index: {index}. {error}')
    return False


def delete_index(index):
    query = f'curl -X DELETE "{elastic_url_}/{index}"'
    result, error = execute_command(query)
    if re.search('acknowledged.*true', result):
        print(f'Deleted index successfully: {index}')
        return True
    print(f'Failed to delete index: {index}. {error}')
    return False


def get_documents_count(index):
    query = f'curl -X GET "{elastic_url_}/{index}/_count"'
    print(f'Executing command: {query}')
    result, error = execute_command(query)
    return str_to_dict(result)['count']


def create_mapping(index):
    query = f"""curl -X PUT "{elastic_url_}/{index}?pretty" -H 'Content-Type: application/json' -d' 
                {{ 
                    "mappings": {{ 
                        "properties": {{ 
                            "log_time":    {{ "type": "date" }},
                            "wait_time":   {{ "type": "integer"  }}
                        }}
                    }}
                }}'"""
    result, error = execute_command(query)
    if re.search('acknowledged.*true', result):
        print(f'Created mapping successfully for index: {index}')
        return True
    print(f'Failed to create mapping for index: {index}')
    print(result)
    return False


def add_date_text(index, date, text):
    query = f"""curl -X POST "{elastic_url_}/{index}/_doc?pretty" -H 'Content-Type: application/json' -d' 
               {{ 
                    "log_time": "{date}", 
                    "wait_time": {text} 
               }}'"""

    result, error = execute_command(query)
    if re.search('result.*created', result):
        print(f'Added date time and text successfully: {date}')
        return True

    print(f'Failed to add date time and text: {date}. {error}')
    print(result)
    return False


def add_doc(index, date, text):
    payload = {
        "log_time": date,
        "wait_time": text
    }

    url = f'{elastic_url_}/{index}/_doc?pretty'
    headers = {
        'content-type': 'application/json',
        'accept': 'application/json'
    }
    response = requests.post(
        url,
        json=payload,
        headers=headers
    )

    if response.status_code == 200:
        print(f'Added document successfully!')
        return True

    print(f'Failed to add document.\n{response.text}')
    return False


if __name__ == '__main__':
    from datetime import datetime, timedelta
    import random

    _index = 'test123'
    # delete_index(index=_index)
    # create_mapping(index=_index)

    for num in range(5):
        timestamp = datetime.now() + timedelta(days=num)
        timestamp = timestamp.strftime(constants.KIBANA_DATE_FORMAT)
        waited_for = random.randint(1, 5)
        for _ in range(random.randint(1, 3)):
            # add_date_text(_index, timestamp, waited_for)
            add_doc(_index, timestamp, waited_for)

    # create_index(index=index)
    # count = get_documents_c/ount(index=_index)
    # print(count)
    # add_date_text(_index, sample_date, 'fourth sample text')
