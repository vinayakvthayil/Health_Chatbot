# backend/utils/gemini_handler.py
import google.generativeai as genai
from typing import Dict, List, Optional
from utils.rag_handler import RAGHandler
from utils.query_decomposer import QueryDecomposer
from utils.search_controller import SearchController
from utils.response_generator import ResponseGenerator
from utils.context_manager import ContextManager
from utils.user_profile_manager import UserProfileManager

class GeminiHandler:
    def __init__(self, config):
        self.config = config
        genai.configure(api_key=config.GOOGLE_API_KEY)
        
        # Initialize components
        self.query_decomposer = QueryDecomposer(config.GOOGLE_API_KEY)
        self.search_controller = SearchController(config.SONAR_API_KEY)
        self.response_generator = ResponseGenerator(config.GOOGLE_API_KEY)
        self.rag_handler = None
        self.context_manager = ContextManager()
        self.user_profile_manager = None
        
        # Initialize chat sessions
        self.chat_sessions: Dict[str, any] = {}

    def set_managers(self, db_manager):
        """Set RAG handler and User Profile Manager"""
        self.rag_handler = RAGHandler(db_manager)
        self.user_profile_manager = UserProfileManager(db_manager)

    async def get_response(
        self, 
        user_id: str, 
        message: str, 
        is_whatsapp: bool = False
    ) -> str:
        """Process user message and generate response"""
        try:
            print(f"\n=== Processing Message for User: {user_id} ===")
            print(f"Original Message: {message}")
            print(f"Platform: {'WhatsApp' if is_whatsapp else 'Streamlit'}")
            
            # Get user profile for WhatsApp users
            user_profile = None
            if is_whatsapp and self.user_profile_manager:
                user_profile = await self.user_profile_manager.get_user_profile(user_id)
            
            # Get session context
            context = self.context_manager.get_context(user_id)
            print(f"Retrieved context length: {len(context)}")
            
            # Step 1: Decompose query and check if research needed
            decomposition_result = self.query_decomposer.decompose_query(message)
            needs_research = decomposition_result['needs_research']
            sub_queries = decomposition_result['sub_queries']
            
            # Step 2: Get research results if needed
            research_results = {}
            if needs_research and sub_queries:
                print("\n=== Conducting Research ===")
                research_results = await self.search_controller.search_research(sub_queries)
            
            # Step 3: Get RAG context
            rag_context = ""
            if self.rag_handler:
                print("\n=== Getting RAG Context ===")
                rag_context = self.rag_handler.get_relevant_context(
                    message,
                    user_profile=user_profile
                )
            
            # Step 4: Generate comprehensive response
            print("\n=== Generating Response ===")
            response = await self.response_generator.generate_response(
                original_query=message,
                sub_queries=sub_queries,
                research_results=research_results,
                rag_context=rag_context,
                user_profile=user_profile
            )
            
            # Step 5: Update context and user profile
            self.context_manager.update_context(user_id, message, response)
            
            if is_whatsapp and self.user_profile_manager:
                context_summary = self.context_manager.get_context_summary(user_id)
                await self.user_profile_manager.update_profile(
                    user_id,
                    message,
                    response,
                    context_summary
                )
            
            print("\n=== Response Generation Complete ===")
            return response
            
        except Exception as e:
            print(f"Error in getting response: {str(e)}")
            return self.config.DEFAULT_RESPONSE

    def clear_context(self, user_id: str):
        """Clear context for a user"""
        self.context_manager.clear_context(user_id)



"""
GeminiHandler: Core AI Integration Manager for Health Chatbot

This class orchestrates the interaction between various components of the chatbot,
managing the flow from user input to AI response generation. It integrates multiple
AI models and services for comprehensive health-related responses.

Key Components:
1. Query Processing:
   - Gemini Flash for query decomposition
   - Perplexity Sonar for research
   - RAG system for local knowledge
   - Context management for conversation history

2. User Management:
   - Separate handling for WhatsApp and Streamlit users
   - User profile management for WhatsApp
   - Session context management for both platforms

Process Flow:
1. Message Reception:
   - Identifies user and platform
   - Retrieves user profile (WhatsApp)
   - Gets conversation context

2. Query Processing:
   - Decomposes complex queries
   - Determines research needs
   - Retrieves relevant context

3. Response Generation:
   - Combines all available information
   - Generates comprehensive response
   - Updates context and profiles

4. Context Management:
   - Maintains conversation history
   - Updates user profiles
   - Handles context clearing

Methods:
1. set_managers(db_manager):
   - Initializes RAG and profile managers
   - Sets up database connections

2. get_response(user_id, message, is_whatsapp):
   - Main processing pipeline
   - Handles complete conversation flow
   - Returns generated response

3. clear_context(user_id):
   - Resets conversation context
   - Cleans up session data

Error Handling:
- Comprehensive try-except blocks
- Detailed error logging
- Fallback responses

Usage:
handler = GeminiHandler(config)
handler.set_managers(db_manager)
response = await handler.get_response("user123", "Hello", False)

Note: Requires proper configuration of API keys and services
in the config file before initialization.
"""
