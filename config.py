import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
API_KEY_OPENAI = os.getenv('API_KEY_OPENAI')
ADMIN_ID = os.getenv('ADMIN_ID')


EMBEDDING_MODEL = 'gpt-3.5-turbo-0125'
