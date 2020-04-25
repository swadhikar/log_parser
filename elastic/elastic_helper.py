from subprocess import Popen, PIPE
import requests
import re

from common import str_to_dict

elastic_host = 'localhost'
elastic_port = 9200
elastic_url_ = f'{elastic_host}:{elastic_port}'


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


def create_log_info_mapping(index):
    query = f"""curl -X PUT "{elastic_url_}/{index}?pretty" -H 'Content-Type: application/json' -d' 
                {{ 
                    "mappings": {{ 
                        "properties": {{ 
                            "timestamp":   {{ "type": "date", "format": "yyyy-MM-dd HH:mm:ss.SSSSSS" }},
                            "level":       {{ "type": "keyword" }}, 
                            "message":     {{ "type": "text" }}, 
                            "app_name":    {{ "type": "keyword" }} 
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


def add_log_info(index, timestamp, level, message, app_name):
    message = message.replace("'", '')  # todo: clean up quotations in the string

    query = f"""curl -X POST "{elastic_url_}/{index}/_doc?pretty" -H "Content-Type: application/json" -d' 
               {{ 
                    "timestamp": "{timestamp}", 
                    "level": "{level}", 
                    "message": "{message}", 
                    "app_name": "{app_name}" 
               }}'"""

    result, error = execute_command(query)
    if re.search('result.*created', result):
        print(f'Added log info successfully for app: {app_name}')
        return True

    print(f'Failed to add below log info.')
    print(f'timestamp: {timestamp}\nlevel: {level}\nmessage: {message}\napp name: {app_name}')
    print(f'Caused by: {error}')
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


# # Must create a mapping at the start of project
log_info_index = 'log_info'
delete_index(log_info_index)  # todo: remove clean up
create_log_info_mapping(log_info_index)

if __name__ == '__main__':
    from datetime import datetime, timedelta
    import random

    # _index = 'log_info'
    # delete_index(index=_index)
    # create_mapping(index=_index)

    # for num in range(5):
    #     timestamp = datetime.now() + timedelta(days=num)
    #     timestamp = timestamp.strftime(constants.KIBANA_DATE_FORMAT)
    #     waited_for = random.randint(1, 5)
    #     for _ in range(random.randint(1, 3)):
    #         # add_date_text(_index, timestamp, waited_for)
    #         add_doc(_index, timestamp, waited_for)

    # create_index(index=index)
    # count = get_documents_c/ount(index=_index)
    # print(count)
    # add_date_text(_index, sample_date, 'fourth sample text')
