import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM_NUMBER, MY_PHONE_NUMBER

def send_sms(message: str, to: str= MY_PHONE_NUMBER):
    """Send an SMS using Twilio."""
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    try:
        message = client.messages.create(
            body=message,
            from_=TWILIO_FROM_NUMBER,
            to=to
        )
        print(f"SMS sent successfully. Message SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send SMS: {e}")

if __name__ == "__main__":
    #send_sms("Hello! This is your first test message.") # Uncomment to test
    pass