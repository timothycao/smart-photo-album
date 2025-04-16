import boto3

rekognition = boto3.client('rekognition')

# Reference: https://docs.aws.amazon.com/rekognition/latest/dg/labels-detect-labels-image.html
def detect_labels(bucket, photo, max_labels=10, min_confidence=75):
    response = rekognition.detect_labels(
        Image={'S3Object': {'Bucket': bucket, 'Name': photo}},
        MaxLabels=max_labels,
        MinConfidence=min_confidence
    )
    # print(response)

    return [label['Name'].lower() for label in response['Labels']]


if __name__ == '__main__':
    bucket = 'cs-gy-9223-smart-photo-album'
    photo = 'HappyFace.jpg'
    print('Detected labels:', detect_labels(bucket, photo))