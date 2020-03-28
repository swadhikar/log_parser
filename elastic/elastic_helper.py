from subprocess import Popen, PIPE
import re

from common import str_to_dict

elastic_host = 'localhost'
elastic_port = 9200
elastic_url_ = f'{elastic_host}:{elastic_port}'
# elastic_url_ = f'https://search-comm-air-metrics-6bn4elbf3jwzp3xk4kdppn2ige.us-east-2.es.amazonaws.com'


def execute_command(command):
    result = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    result, error = result.communicate()
    return result.decode('utf-8'), error


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
                            "text":   {{ "type": "text"  }}
                        }}
                    }}
                }}'"""
    result, error = execute_command(query)
    print(result)
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
                    "text": "{text}" 
               }}'"""

    result, error = execute_command(query)
    if re.search('result.*created', result):
        print(f'Added date time and text successfully: {date}')
        return True

    print(f'Failed to add date time and text: {date}')
    print(result)
    return False


if __name__ == '__main__':
    _index = 'test123'
    sample_date = '2015-01-02T12:10:30Z'
    # create_index(index=index)
    # count = get_documents_count(index=index)
    # print(count)
    # delete_index(index=index)
    # create_mapping(index)
    add_date_text(_index, sample_date, 'second sample text that should be stored!')
