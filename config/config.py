import os
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


# OpenSearch
OPENSEARCH_URL = os.getenv('OPENSEARCH_URL')
OPENSEARCH_HEADERS = {'Content-Type': 'application/json'}
OPENSEARCH_AUTH = (os.getenv('OPENSEARCH_USERNAME'), os.getenv('OPENSEARCH_PASSWORD'))


# Lex
LEX_BOT_ID = os.getenv('LEX_BOT_ID')
LEX_BOT_ALIAS_ID = os.getenv('LEX_BOT_ALIAS_ID')
LEX_LOCALE_ID = os.getenv('LEX_LOCALE_ID')