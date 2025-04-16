import requests
from config.config import OPENSEARCH_URL, OPENSEARCH_HEADERS, OPENSEARCH_AUTH


def insert_photo(photo):
    url = f"{OPENSEARCH_URL}/photos/_doc/{photo['objectKey']}"

    response = requests.put(
        url,
        headers=OPENSEARCH_HEADERS,
        auth=OPENSEARCH_AUTH,
        json=photo
    )

    if response.status_code in [200, 201]:
        print(f"Indexed: {photo.get('objectKey', '')} - {photo.get('labels', [])}")
    else:
        print(f"Error indexing {photo.get('objectKey', '')}: {response.status_code} - {response.text}")


if __name__ == '__main__':
    photo = {
        'objectKey': 'my-photo.jpg',
        'bucket': 'my-photo-bucket',
        'createdTimestamp': '2025-01-01T00:00:00',
        'labels': ['person', 'dog', 'ball', 'park']
    }
    insert_photo(photo)