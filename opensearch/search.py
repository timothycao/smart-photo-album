import requests
from config.config import OPENSEARCH_URL, OPENSEARCH_HEADERS, OPENSEARCH_AUTH

def search_photos(labels):
    url = f'{OPENSEARCH_URL}/photos/_search'

    query = {
        'query': {
            'terms': {
                'labels': labels
            }
        }
    }

    response = requests.get(
        url,
        headers=OPENSEARCH_HEADERS,
        auth=OPENSEARCH_AUTH,
        json=query
    )
    # print(response.json())

    if response.status_code == 200:
        hits = response.json().get('hits', {}).get('hits', [])
        return [hit['_source'] for hit in hits]
    else:
        print(f'Error searching: {response.status_code} - {response.text}')


if __name__ == '__main__':
    labels = ['happy', 'face']
    print(search_photos(labels))