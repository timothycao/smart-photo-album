import json
from datetime import datetime, timezone
from opensearch.insert import insert_photo


def lambda_handler(event, context):
    # Extract bucket name and object key
    s3 = event['Records'][0]['s3']
    bucket = s3['bucket']['name']
    object_key = s3['object']['key']
    
    # Get the current timestamp
    timestamp = datetime.now(timezone.utc).isoformat()

    # Get image labels
    labels = ['person', 'happy', 'face']    # placeholder labels

    # Construct the photo object
    photo = {
        'objectKey': object_key,
        'bucket': bucket,
        'createdTimestamp': timestamp,
        'labels': labels
    }

    # Insert the photo into OpenSearch
    insert_photo(photo)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }


if __name__ == '__main__':
    # Sample s3:ObjectCreated:Put event message
    # Reference: https://docs.aws.amazon.com/AmazonS3/latest/userguide/notification-content-structure.html
    event = {
        'Records': [
            {
                's3': {
                    'bucket': {
                        'name': 'amzn-s3-demo-bucket'
                    },
                    'object': {
                        'key': 'HappyFace.jpg'
                    }
                }
            }
        ]
    }
    lambda_handler(event, None)