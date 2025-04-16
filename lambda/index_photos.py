import json
from datetime import datetime, timezone
from s3.metadata import get_custom_labels
from rekognition.detect import detect_labels
from opensearch.insert import insert_photo


def lambda_handler(event, context):
    # Extract bucket name and object key
    s3 = event['Records'][0]['s3']
    bucket = s3['bucket']['name']
    object_key = s3['object']['key']
    
    # Get the current timestamp
    timestamp = datetime.now(timezone.utc).isoformat()

    # Get custom labels from S3 metadata
    custom_labels = get_custom_labels(bucket, object_key)

    # Get detected labels using Rekognition
    detected_labels = detect_labels(bucket, object_key)

    # Combine custom and detected labels (removing duplicates)
    all_labels = list(set(custom_labels + detected_labels))

    # Construct the photo object
    photo = {
        'objectKey': object_key,
        'bucket': bucket,
        'createdTimestamp': timestamp,
        'labels': all_labels
    }

    # Insert the photo into OpenSearch
    insert_photo(photo)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


if __name__ == '__main__':
    # Reference: https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-content-structure.html
    # Sample s3:ObjectCreated:Put event message
    event = {
        'Records': [
            {
                's3': {
                    'bucket': {
                        'name': 'cs-gy-9223-smart-photo-album'
                    },
                    'object': {
                        'key': 'HappyFace.jpg'
                    }
                }
            }
        ]
    }
    lambda_handler(event, None)