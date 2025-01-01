from typing import Dict, List, Optional
import json
from datetime import datetime

class ContextManager:
    def __init__(self):
        self.session_contexts = {}
    
    def update_context(self, session_id: str, message: str, response: str):
        """Update context for a session"""
        if session_id not in self.session_contexts:
            self.session_contexts[session_id] = {
                "messages": [],
                "summary": "",
                "last_update": None
            }
        
        # Add new message to context
        self.session_contexts[session_id]["messages"].append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now().isoformat()
        })
        self.session_contexts[session_id]["messages"].append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 10 messages
        if len(self.session_contexts[session_id]["messages"]) > 20:  # 10 exchanges
            self.session_contexts[session_id]["messages"] = self.session_contexts[session_id]["messages"][-20:]
        
        self.session_contexts[session_id]["last_update"] = datetime.now().isoformat()
    
    def get_context(self, session_id: str, limit: int = 5) -> List[Dict]:
        """Get recent context for a session"""
        if session_id not in self.session_contexts:
            return []
        
        messages = self.session_contexts[session_id]["messages"]
        return messages[-limit*2:] if messages else []  # Return last 'limit' exchanges
    
    def get_context_summary(self, session_id: str) -> str:
        """Get summary of context"""
        if session_id not in self.session_contexts:
            return ""
        
        messages = self.session_contexts[session_id]["messages"]
        if not messages:
            return ""
        
        # Create a simple summary of the conversation
        summary = []
        for msg in messages[-6:]:  # Last 3 exchanges
            if msg["role"] == "user":
                summary.append(f"User asked about: {msg['content'][:50]}...")
            else:
                summary.append(f"Bot provided information about: {msg['content'][:50]}...")
        
        return "\n".join(summary)
    
    def clear_context(self, session_id: str):
        """Clear context for a session"""
        if session_id in self.session_contexts:
            del self.session_contexts[session_id]



"""
ContextManager: Session Context Management System for Health Chatbot

This class manages conversation context for both Streamlit and WhatsApp interfaces,
maintaining a temporary memory of conversations and generating summaries for context-aware
responses.

Key Features:
1. Session Management:
   - Maintains separate contexts for each user session
   - Stores both user and assistant messages
   - Timestamps all interactions
   - Limits context size for memory efficiency

2. Context Operations:
   - Update: Adds new messages to context
   - Retrieve: Gets recent conversation history
   - Summarize: Creates brief conversation summaries
   - Clear: Removes session context

Data Structure:
self.session_contexts = {
    "session_id": {
        "messages": [
            {
                "role": "user/assistant",
                "content": "message text",
                "timestamp": "ISO format datetime"
            }
        ],
        "summary": "conversation summary",
        "last_update": "ISO format datetime"
    }
}

Methods:
1. update_context(session_id, message, response):
   - Adds new message-response pair to session context
   - Maintains rolling window of last 10 exchanges (20 messages)
   - Updates last_update timestamp

2. get_context(session_id, limit=5):
   - Retrieves recent conversation history
   - Returns last 'limit' exchanges (user-assistant pairs)
   - Returns empty list for new sessions

3. get_context_summary(session_id):
   - Creates readable summary of recent conversation
   - Uses last 3 exchanges (6 messages)
   - Truncates long messages for clarity

4. clear_context(session_id):
   - Removes all context for specified session
   - Used for session cleanup or reset

Usage:
context_manager = ContextManager()
context_manager.update_context("user123", "Hello", "Hi there!")
recent_context = context_manager.get_context("user123")
summary = context_manager.get_context_summary("user123")

Note: This is an in-memory storage system. Context is lost when server restarts.
For persistent storage, consider using ChromaDB or another database solution.
"""