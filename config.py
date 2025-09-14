import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_FROM_NUMBER = os.getenv('TWILIO_FROM_NUMBER')
MY_PHONE_NUMBER = os.getenv('MY_PHONE_NUMBER')

# Verfy that all necessary environment variables are set
if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, MY_PHONE_NUMBER]):
    raise EnvironmentError("One or more Twilio environment variables are not set in the .env file.")