import boto3

s3 = boto3.client('s3')

# Reference: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3/client/head_object.html
def get_custom_labels(bucket, photo):
    response = s3.head_object(
        Bucket=bucket,
        Key=photo
    )
    # print(response)

    # Reference: https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingMetadata.html#UserMetadata
    # User-defined metadata key begins with `x-amz-meta-` (assume key here was `x-amz-meta-customLabels`)
    metadata = response.get('Metadata', {})
    custom_labels = metadata.get('customlabels', '')    # S3 stores these keys in lowercase ('customlabels')

    return [label.strip().lower() for label in custom_labels.split(',')] if custom_labels else []


if __name__ == '__main__':
    bucket = 'cs-gy-9223-smart-photo-album'
    photo = 'HappyFace.jpg'
    print('Custom labels:', get_custom_labels(bucket, photo))