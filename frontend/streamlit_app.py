# frontend/streamlit_app.py
import streamlit as st
import requests
import json
from datetime import datetime
import time

# Configure Streamlit page
st.set_page_config(
    page_title="Health Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
API_URL = "http://localhost:5000"

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_id' not in st.session_state:
    st.session_state.user_id = f"streamlit_{int(time.time())}"
if 'session_start' not in st.session_state:
    st.session_state.session_start = datetime.now()

def get_random_tip():
    """Fetch random health tip from API"""
    try:
        response = requests.get(f"{API_URL}/tips/random")
        return response.json()
    except Exception as e:
        st.error(f"Error fetching health tip: {str(e)}")
        return None

def send_message(message):
    """Send chat message to API"""
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={
                "user_id": st.session_state.user_id,
                "message": message
            }
        )
        return response.json()
    except Exception as e:
        st.error(f"Error sending message: {str(e)}")
        return None

def submit_feedback(rating, comment):
    """Submit user feedback to API"""
    try:
        response = requests.post(
            f"{API_URL}/feedback",
            json={
                "user_id": st.session_state.user_id,
                "rating": rating,
                "comment": comment
            }
        )
        return response.json()
    except Exception as e:
        st.error(f"Error submitting feedback: {str(e)}")
        return None

def clear_chat_context():
    """Clear chat context"""
    try:
        response = requests.post(
            f"{API_URL}/clear-context",
            json={"user_id": st.session_state.user_id}
        )
        if response.status_code == 200:
            st.session_state.messages = []
            return True
    except Exception as e:
        st.error(f"Error clearing context: {str(e)}")
    return False

# Sidebar
with st.sidebar:
    st.title("🏥 Health Assistant")
    
    # Display random health tip
    st.subheader("Daily Health Tip")
    if st.button("Get New Tip"):
        tip = get_random_tip()
        if tip:
            st.info(tip['tip'])
            if tip.get('related_products'):
                st.subheader("Related Products")
                for product in tip['related_products']:
                    st.write(f"📦 {product['name']} - ${product['price']}")
                    st.write(product['description'])
    
    # Feedback section
    st.subheader("Feedback")
    rating = st.slider("Rate your experience", 1, 5, 3)
    feedback_comment = st.text_area("Your feedback")
    if st.button("Submit Feedback"):
        if submit_feedback(rating, feedback_comment):
            st.success("Thank you for your feedback!")
    
    # Clear context button
    if st.button("Clear Chat History"):
        if clear_chat_context():
            st.success("Chat history cleared!")

# Main chat interface
st.title("💬 Chat with Health Assistant")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get bot response
    response = send_message(prompt)
    if response:
        # Add assistant response to chat history
        assistant_response = response.get('response', "I'm sorry, I couldn't process that request.")
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        with st.chat_message("assistant"):
            st.markdown(assistant_response)

# Footer
st.markdown("---")
st.markdown("Need help? Use the feedback form in the sidebar to reach out to our team.")






"""
Streamlit Frontend: User Interface for Health Chatbot

This application provides the web interface for the health chatbot, implementing
all MVP requirements including chat interface, health tips, feedback system,
and session management.

Key Features:

1. User Interface Components:
   - Chat interface with history
   - Health tips display
   - Feedback collection
   - Session management

2. Session State Management:
   - Message history
   - User identification
   - Session timing
   - Context maintenance

3. API Integration:
   - Chat message handling
   - Health tip retrieval
   - Feedback submission
   - Context management

4. Error Handling:
   - API communication errors
   - Display errors
   - Session errors
   - Network issues

Layout Structure:
1. Sidebar:
   - Health Assistant title
   - Daily health tip
   - Feedback system
   - Clear chat option

2. Main Area:
   - Chat interface
   - Message history
   - Input field
   - Response display

Functions:
1. get_random_tip():
   - Fetches health tips
   - Handles API errors
   - Displays related products

2. send_message():
   - Manages chat communication
   - Handles API requests
   - Updates chat history

3. submit_feedback():
   - Collects user feedback
   - Sends to backend
   - Shows confirmation

4. clear_chat_context():
   - Resets chat history
   - Clears session state
   - Updates UI

Session Management:
- Unique user identification
- Message history tracking
- Session timing
- State persistence

Error Handling:
- API communication errors
- Display fallbacks
- User notifications
- Graceful degradation

Note: This frontend implements all MVP requirements:
- Initial engagement (health tips)
- Chat interface
- Feedback system
- Session management
- Error handling
"""