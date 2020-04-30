from subprocess import Popen, PIPE
import requests
import re

from common import str_to_dict

# Todo: Need to place the configurations in config
elastic_host = 'localhost'
elastic_port = 9200
elastic_url_ = f'{elastic_host}:{elastic_port}'


def execute_command(command):
    result = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    result, error = result.communicate()
    return result.decode('utf-8'), error.decode('utf-8')


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


# # Note:
# #   Lines 80-83 should be run only on first time execution
# #   Must create a mapping at the start of project
# log_info_index = 'log_info'
# delete_index(log_info_index)  # todo: remove clean up
# create_log_info_mapping(log_info_index)
