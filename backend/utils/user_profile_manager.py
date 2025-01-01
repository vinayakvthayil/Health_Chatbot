from typing import Dict, List, Optional
from datetime import datetime
import json

class UserProfileManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.collection_name = "user_profiles"
    
    async def get_user_profile(self, user_id: str) -> Dict:
        """Get user profile from database"""
        try:
            profile = self.db_manager.get_user_profile(user_id)
            if not profile:
                # Create default profile
                profile = {
                    "user_id": user_id,
                    "summary": "",
                    "key_topics": [],
                    "health_concerns": [],
                    "preferences": {"language": "en"},
                    "created_at": datetime.now().isoformat(),
                    "last_interaction": datetime.now().isoformat()
                }
                self.db_manager.store_user_profile(user_id, profile)
            
            return profile
            
        except Exception as e:
            print(f"Error getting user profile: {str(e)}")
            return self._create_default_profile(user_id)
    
    async def update_profile(
        self, 
        user_id: str, 
        message: str, 
        response: str,
        context_summary: Optional[str] = None
    ):
        """Update user profile with new interaction"""
        try:
            profile = await self.get_user_profile(user_id)
            
            # Update last interaction
            profile["last_interaction"] = datetime.now().isoformat()
            
            # Update summary if provided
            if context_summary:
                profile["summary"] = context_summary
            
            # Extract and update key topics
            topics = self._extract_topics(message, response)
            if topics:
                profile["key_topics"] = list(set(profile["key_topics"] + topics))
            
            # Store updated profile
            self.db_manager.store_user_profile(user_id, profile)
            
            return profile
            
        except Exception as e:
            print(f"Error updating user profile: {str(e)}")
            return self._create_default_profile(user_id)
    
    def _create_default_profile(self, user_id: str) -> Dict:
        """Create default user profile"""
        return {
            "user_id": user_id,
            "summary": "",
            "key_topics": [],
            "health_concerns": [],
            "preferences": {"language": "en"},
            "created_at": datetime.now().isoformat(),
            "last_interaction": datetime.now().isoformat()
        }
    
    def _extract_topics(self, message: str, response: str) -> List[str]:
        """Extract key topics from message and response"""
        # Simple keyword-based topic extraction
        health_topics = [
            "sleep", "stress", "anxiety", "diet", "exercise",
            "nutrition", "supplements", "meditation", "wellness"
        ]
        
        found_topics = []
        combined_text = (message + " " + response).lower()
        
        for topic in health_topics:
            if topic in combined_text:
                found_topics.append(topic)
        
        return found_topics
    



"""
UserProfileManager: User Profile Management System for Health Chatbot

This class manages user profiles for WhatsApp users, maintaining interaction
history, preferences, and topic tracking. It provides persistent storage and
retrieval of user information for personalized interactions.

Key Features:
1. Profile Management:
   - Create and retrieve profiles
   - Update interaction history
   - Track health topics
   - Manage user preferences

2. Topic Tracking:
   - Extract health-related topics
   - Update user interests
   - Maintain topic history

Data Structure:
user_profile = {
    "user_id": str,          # Unique identifier
    "summary": str,          # Interaction summary
    "key_topics": List[str], # Health topics discussed
    "health_concerns": List[str], # Specific health issues
    "preferences": {         # User preferences
        "language": str      # Communication language
    },
    "created_at": str,      # Profile creation timestamp
    "last_interaction": str  # Last interaction timestamp
}

Methods:
1. get_user_profile(user_id):
   - Retrieves existing profile
   - Creates default if none exists
   - Handles database errors

2. update_profile(user_id, message, response, context_summary):
   - Updates interaction timestamp
   - Updates conversation summary
   - Extracts and updates topics
   - Stores changes in database

3. _create_default_profile(user_id):
   - Creates new profile structure
   - Sets default values
   - Initializes timestamps

4. _extract_topics(message, response):
   - Analyzes conversation text
   - Identifies health topics
   - Updates topic tracking

Error Handling:
- Database operation errors
- Profile creation failures
- Update operation errors
- Topic extraction issues

Usage Example:
manager = UserProfileManager(db_manager)
profile = await manager.get_user_profile("user123")
updated = await manager.update_profile(
    "user123",
    "How can I sleep better?",
    "Here are some sleep tips...",
    "User interested in sleep improvement"
)

Note: This component is crucial for:
- Personalized responses
- Context awareness
- User history tracking
- Topic-based customization
"""