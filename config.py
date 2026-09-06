# Configuration
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', 'YOUR_BOT_TOKEN_HERE')
TELEGRAM_ADMIN_ID = int(os.getenv('TELEGRAM_ADMIN_ID', '0'))

# API Endpoints
API_BASE_URL = 'https://api.pangtiger.com/hall/userverse/api/v1'
BIND_ACCOUNT_ENDPOINT = f'{API_BASE_URL}/bind/custom-account'
BIND_PHONE_ENDPOINT = f'{API_BASE_URL}/bind/phone'
VERIFY_OTP_ENDPOINT = f'{API_BASE_URL}/verify-code/user/phone'

# Database
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///bot_data.db')

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
