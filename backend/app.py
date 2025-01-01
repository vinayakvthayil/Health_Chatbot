# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.gemini_handler import GeminiHandler
from utils.twilio_handler import TwilioHandler
from database.chromadb_manager import ChromaDBManager
from services.health_tips import HealthTipsService
from config import Config
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load configuration
config = Config()

# Initialize handlers
gemini_handler = GeminiHandler(config)
twilio_handler = TwilioHandler()
db_manager = ChromaDBManager(config.CHROMA_DB_PATH)

# Initialize services
gemini_handler.set_managers(db_manager)
health_tips_service = HealthTipsService(db_manager)

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Health chatbot API is running",
        "features": {
            "chat": True,
            "whatsapp": config.WHATSAPP_ENABLED,
            "tips": True,
            "feedback": True
        }
    })

@app.route('/chat', methods=['POST'])
async def chat():
    """Handle chat messages"""
    try:
        data = request.json
        user_id = data.get('user_id', 'default_user')
        message = data.get('message')
        
        if not message:
            return jsonify({"error": "Message is required"}), 400

        # Get response from Gemini
        response = await gemini_handler.get_response(
            user_id=user_id,
            message=message,
            is_whatsapp=False
        )
        
        # Store chat history
        db_manager.store_chat(user_id, message, response)
        
        return jsonify({
            "response": response,
            "user_id": user_id
        })

    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": "Failed to process chat message"}), 500

@app.route('/whatsapp/webhook', methods=['POST'])
async def whatsapp_webhook():
    """Handle WhatsApp messages"""
    try:
        # Get incoming WhatsApp message details
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '').strip()
        
        print(f"Received WhatsApp message: {incoming_msg} from {sender}")
        
        if not incoming_msg:
            return twilio_handler.create_response("Message is required")

        # Get response from Gemini
        response = await gemini_handler.get_response(
            user_id=sender,
            message=incoming_msg,
            is_whatsapp=True
        )
        
        # Create and return WhatsApp response
        return twilio_handler.create_response(response)

    except Exception as e:
        print(f"Error in WhatsApp webhook: {str(e)}")
        return twilio_handler.create_response(config.DEFAULT_RESPONSE)

@app.route('/whatsapp/status', methods=['POST'])
def whatsapp_status():
    """Handle WhatsApp message status updates"""
    try:
        message_sid = request.values.get('MessageSid', '')
        message_status = request.values.get('MessageStatus', '')
        
        print(f"Message {message_sid} status: {message_status}")
        
        return jsonify({
            "status": "success",
            "message": f"Status update received: {message_status}"
        })
        
    except Exception as e:
        print(f"Error in status webhook: {str(e)}")
        return jsonify({"error": "Failed to process status update"}), 500

@app.route('/tips/random', methods=['GET'])
def get_random_tip():
    """Get random health tip"""
    try:
        category = request.args.get('category')
        tip = health_tips_service.get_random_tip(category)
        
        return jsonify({
            "tip": tip.get('tip', config.DEFAULT_RESPONSE),
            "category": tip.get('category', "general_health"),
            "related_products": tip.get('related_products', [])
        })
    except Exception as e:
        print(f"Error in random tip endpoint: {str(e)}")
        return jsonify({
            "tip": config.DEFAULT_RESPONSE,
            "category": "general_health",
            "related_products": []
        })

@app.route('/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback"""
    try:
        data = request.json
        user_id = data.get('user_id', 'default_user')
        rating = data.get('rating')
        comment = data.get('comment', '')
        
        if rating is None:
            return jsonify({"error": "Rating is required"}), 400

        # Store feedback
        db_manager.store_feedback(user_id, rating, comment)
        
        return jsonify({
            "message": "Thank you for your feedback!",
            "status": "success"
        })
    except Exception as e:
        print(f"Error in feedback endpoint: {str(e)}")
        return jsonify({"error": "Failed to process feedback"}), 500

@app.route('/clear-context', methods=['POST'])
def clear_context():
    """Clear user context"""
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
            
        gemini_handler.clear_context(user_id)
        
        return jsonify({
            "message": "Context cleared successfully",
            "status": "success"
        })
    except Exception as e:
        print(f"Error clearing context: {str(e)}")
        return jsonify({"error": "Failed to clear context"}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)




"""
Flask Application: Main Server Component for Health Chatbot

This is the core server application that integrates all components and provides
REST API endpoints for both Streamlit frontend and WhatsApp integration. It manages
all incoming requests, route handling, and response generation.

Key Components:
1. Service Integration:
   - Gemini AI for response generation
   - Twilio for WhatsApp communication
   - ChromaDB for data storage
   - Health Tips service for random tips

2. API Endpoints:
   a. Core Functionality:
      - /health: System health check
      - /chat: Main chat interface
      - /tips/random: Random health tip generator
      - /feedback: User feedback collection
      - /clear-context: Context management

   b. WhatsApp Integration:
      - /whatsapp/webhook: Message handler
      - /whatsapp/status: Status updates

3. Error Handling:
   - 404 Not Found handler
   - 500 Internal Server Error handler
   - Per-endpoint error management
   - Detailed error logging

Endpoint Details:

1. /health (GET):
   - System status check
   - Feature availability status
   - WhatsApp integration status

2. /chat (POST):
   - Handles chat messages
   - User identification
   - Response generation
   - Chat history storage

3. /whatsapp/webhook (POST):
   - WhatsApp message processing
   - Sender identification
   - Response generation
   - WhatsApp-specific formatting

4. /tips/random (GET):
   - Random health tip generation
   - Category-based filtering
   - Product recommendations
   - Error handling

5. /feedback (POST):
   - User feedback collection
   - Rating processing
   - Comment storage
   - Success confirmation

6. /clear-context (POST):
   - Context clearing
   - User session management
   - Success confirmation

Configuration:
- CORS enabled for cross-origin requests
- Debug mode for development
- Local host binding
- Port 5000

Error Management:
- Request validation
- Error status codes
- Detailed error messages
- Exception handling

Usage:
1. Development:
   python app.py
   
2. API Interaction:
   - Use Postman/curl for testing
   - Frontend integration via fetch/axios
   - WhatsApp through Twilio webhooks

Note: This application serves as the central hub for:
- Frontend communication
- WhatsApp integration
- AI response generation
- Data storage and retrieval
- User interaction management

Security Considerations:
- Input validation
- Error message sanitization
- Rate limiting (to be implemented)
- Authentication (for future)
"""