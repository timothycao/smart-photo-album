import uuid
import boto3
from config.config import LEX_BOT_ID, LEX_BOT_ALIAS_ID, LEX_LOCALE_ID


# Initialize Lex Client
lex_client = boto3.client('lexv2-runtime')


def extract_keywords(query):
    try:
        # Gererate a unique session ID
        session_id = str(uuid.uuid4())

        response = lex_client.recognize_text(
            botId=LEX_BOT_ID,
            botAliasId=LEX_BOT_ALIAS_ID,
            localeId=LEX_LOCALE_ID,
            sessionId=session_id,
            text=query
        )

    except Exception as e:
        print(f'Failed to connect to Lex: {e}')
        return []
    
    try:
        # print(response)
        slots = response.get('sessionState', {}).get('intent', {}).get('slots', {})
        label_slot = slots.get('Label', {})
        values = label_slot.get('values', [])

        return [value['value']['interpretedValue'].lower() for value in values]
    
    except Exception as e:
        print(f'Failed to extract keywords: {e}')
        return []


if __name__ == '__main__':
    query = 'Show me photos of people with happy faces'
    print(extract_keywords(query))