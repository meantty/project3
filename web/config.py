import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    DASH_DEBUG = True
