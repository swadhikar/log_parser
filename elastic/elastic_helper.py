"""
curl -X POST "localhost:9200/twitter/_doc/?pretty" -H 'Content-Type: application/json' -d'
{
    "user" : "swadhi",
    "post_date" : "2020-11-15T14:12:12",
    "message" : "trying out Elasticsearch"
}
'
"""
from subprocess import Popen, PIPE
import re

# elastic_host = 'localhost'
# elastic_port = 9200
# elastic_url_ = f'{elastic_host}:{elastic_port}'
elastic_url_ = f'https://search-comm-air-metrics-6bn4elbf3jwzp3xk4kdppn2ige.us-east-2.es.amazonaws.com/'


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


def get_documents_count(index):
    pass


if __name__ == '__main__':
    create_index('test123')
