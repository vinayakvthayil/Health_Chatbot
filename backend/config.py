# backend/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    SONAR_API_KEY = os.getenv('SONAR_API_KEY')
    FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
    
    # Database Configuration
    CHROMA_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'chromadb')
    
    # Model Configuration
    GEMINI_FLASH_MODEL = "gemini-1.5-flash"
    GEMINI_PRO_MODEL = "gemini-1.5-pro"
    SONAR_MODEL = "llama-3.1-sonar-small-128k-online"
    
    # Chat Configuration
    MAX_CHAT_HISTORY = 10
    MAX_SUB_QUERIES = 4
    
    # Response Configuration
    DEFAULT_RESPONSE = "I apologize, but I'm having trouble processing your request. Please try again."
    SAFETY_WARNING = "For your safety, please consult a healthcare professional for accurate advice."
    
    # Session Configuration
    STREAMLIT_SESSION_TIMEOUT = 3600  # 1 hour in seconds
    
    # WhatsApp Configuration
    WHATSAPP_ENABLED = bool(os.getenv('TWILIO_ACCOUNT_SID') and 
                           os.getenv('TWILIO_AUTH_TOKEN') and 
                           os.getenv('TWILIO_WHATSAPP_NUMBER'))
    


"""
Configuration Manager: Central Configuration System for Health Chatbot

This class manages all configuration settings for the application, including API keys,
model settings, and various operational parameters. It uses environment variables for
sensitive information and provides default values for other settings.

Configuration Categories:

1. API Keys and Authentication:
   - Google Gemini API
   - Perplexity Sonar API
   - Flask Secret Key
   - Twilio Credentials (WhatsApp)

2. Database Settings:
   - ChromaDB path configuration
   - Persistent storage location
   - Database structure settings

3. Model Configuration:
   - Gemini Flash (fast queries)
   - Gemini Pro (detailed responses)
   - Sonar Model (research queries)

4. Chat Settings:
   - Maximum chat history
   - Maximum sub-queries
   - Response limitations

5. Response Templates:
   - Default error responses
   - Safety warnings
   - System messages

6. Session Management:
   - Timeout settings
   - Session persistence
   - State management

7. WhatsApp Integration:
   - Feature toggle
   - Credential validation
   - Number configuration

Required Environment Variables (.env):
```plaintext
GOOGLE_API_KEY=your_gemini_api_key
SONAR_API_KEY=your_sonar_api_key
FLASK_SECRET_KEY=your_secret_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_WHATSAPP_NUMBER=your_whatsapp_number

Usage:
Load environment variables
Initialize configuration
Access settings throughout application
Security Features:
Environment variable usage
Credential validation
Safe defaults
Error handling
Note: This configuration system ensures:
Secure credential management
Consistent settings across app
Easy maintenance and updates
Environment-specific configuration
"""
