import os
from dotenv import load_dotenv
import boto3


# Load environment variables from .env
load_dotenv()


# S3
s3_client = boto3.client('s3')


# Rekognition
rekognition_client = boto3.client('rekognition')


# OpenSearch
opensearch_client = boto3.client('opensearch')
OPENSEARCH_URL = f"https://{opensearch_client.describe_domain(DomainName='photos')['DomainStatus']['EndpointV2']}"
OPENSEARCH_HEADERS = {'Content-Type': 'application/json'}
OPENSEARCH_AUTH = (os.getenv('OPENSEARCH_USERNAME'), os.getenv('OPENSEARCH_PASSWORD'))


# Lex
lex_client = boto3.client('lexv2-runtime')
lex = boto3.client('lexv2-models')
LEX_BOT_ID = lex.list_bots(filters=[{'name': 'BotName', 'values': ['PhotoSearchBot'], 'operator': 'EQ'}])['botSummaries'][0]['botId']
LEX_BOT_ALIAS_ID = lex.list_bot_aliases(botId=LEX_BOT_ID)['botAliasSummaries'][0]['botAliasId']
LEX_LOCALE_ID = 'en_US'