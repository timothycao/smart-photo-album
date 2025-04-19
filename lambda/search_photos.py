import json
from opensearch.search import search_photos
from lex.extract import extract_keywords


# API spec: https://github.com/001000001/ai-photo-search-columbia-f2018/blob/master/swagger.yaml
def format_results(photos):
    # Format search results as per the API spec
    results = []
    for photo in photos:
        object_key = photo['objectKey']
        bucket = photo['bucket']
        labels = photo['labels']
        
        results.append({
            'url': f'https://{bucket}.s3.amazonaws.com/{object_key}',
            'labels': labels
        })
    
    return results


def lambda_handler(event, context):
    # Format response as per the API spec
    try:
        # Extract query
        query = event.get('queryStringParameters', {}).get('q', '')

        # Get keywords using Lex
        keywords = extract_keywords(query)
        
        # Query OpenSearch
        photos = search_photos(keywords)

        # Format results
        results = format_results(photos)

        # Return 200 response
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin': '*' },
            'body': json.dumps({'results': results})
        }
    
    except Exception as e:
        # Return 500 response
        return {
            'statusCode': 500,
            'headers': { 'Access-Control-Allow-Origin': '*' },
            'body': json.dumps({'code': 500, 'message': 'Internal Server Error'})
        }


if __name__ == '__main__':
    # Reference: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
    # Sample API Gateway event message
    event = {
        'queryStringParameters': {
            # 'q': 'Show me photos of dogs and cats'
            'q': 'Show me photos of people with happy faces'
        }
    }
    print(lambda_handler(event, None))