import requests
from config.config import OPENSEARCH_URL, OPENSEARCH_HEADERS, OPENSEARCH_AUTH


def create_index():
    url = f'{OPENSEARCH_URL}/photos'

    index_config = {
        'settings': {
            'number_of_shards': 1,
            'number_of_replicas': 1
        },
        'mappings': {
            'properties': {
                'objectKey': { 'type': 'keyword' },
                'bucket': { 'type': 'keyword' },
                'createdTimestamp': { 'type': 'date' },
                'labels': { 'type': 'keyword' }
            }
        }
    }

    response = requests.put(url, json=index_config, headers=OPENSEARCH_HEADERS, auth=OPENSEARCH_AUTH)

    if response.status_code in [200, 201]:
        print(f'Index "photos" created successfully')
    else:
        print(f'Error creating index: {response.status_code} - {response.text}')


if __name__ == '__main__':
    create_index()