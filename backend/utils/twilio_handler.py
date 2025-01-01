from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os
from dotenv import load_dotenv

class TwilioHandler:
    def __init__(self):
        load_dotenv()
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
        
        if all([self.account_sid, self.auth_token, self.whatsapp_number]):
            self.client = Client(self.account_sid, self.auth_token)
        else:
            print("Warning: Twilio credentials not found in .env file")
            self.client = None

    def send_whatsapp_message(self, to_number: str, message: str) -> bool:
        """Send WhatsApp message using Twilio"""
        try:
            if not self.client:
                print("Error: Twilio client not initialized")
                return False

            message = self.client.messages.create(
                from_=f'whatsapp:{self.whatsapp_number}',
                body=message,
                to=f'whatsapp:{to_number}'
            )
            
            return True
        except Exception as e:
            print(f"Error sending WhatsApp message: {str(e)}")
            return False

    def create_response(self, message: str) -> str:
        """Create TwiML response for incoming messages"""
        try:
            resp = MessagingResponse()
            resp.message(message)
            return str(resp)
        except Exception as e:
            print(f"Error creating response: {str(e)}")
            return ""
        


"""
TwilioHandler: WhatsApp Integration Manager for Health Chatbot

This class manages WhatsApp communication through Twilio's API, handling both
outgoing messages and incoming webhook responses. It provides a reliable
interface for WhatsApp integration with proper error handling.

Key Features:
1. Message Handling:
   - Send WhatsApp messages
   - Create webhook responses
   - Handle message formatting

2. Configuration:
   - Environment variable loading
   - Credential management
   - WhatsApp number configuration

Required Environment Variables:
TWILIO_ACCOUNT_SID: Your Twilio account SID
TWILIO_AUTH_TOKEN: Your Twilio auth token
TWILIO_WHATSAPP_NUMBER: Your WhatsApp number

Methods:
1. send_whatsapp_message(to_number, message):
   - Sends message to specified WhatsApp number
   - Handles formatting and delivery
   - Returns success/failure status

2. create_response(message):
   - Creates TwiML response for webhooks
   - Formats response for Twilio
   - Handles error cases

Error Handling:
- Credential validation
- Client initialization checks
- Message sending errors
- Response creation errors

Usage Example:
handler = TwilioHandler()
success = handler.send_whatsapp_message(
    "+1234567890",
    "Hello from Health Chatbot!"
)

Webhook Response:
response = handler.create_response("Thank you for your message")

Note: Requires proper Twilio setup:
1. Valid Twilio account
2. WhatsApp sandbox or business API
3. Proper environment variables
4. Webhook configuration
"""