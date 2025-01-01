import chromadb
from chromadb.utils import embedding_functions
import os
from datetime import datetime
from typing import Dict, List, Optional

class ChromaDBManager:
    def __init__(self, persist_directory: str):
        self.persist_directory = persist_directory
        # Ensure directory exists
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize embedding function
        self.embedding_function = embedding_functions.DefaultEmbeddingFunction()
        
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Create collections with embedding function
        self.health_tips = self.client.get_or_create_collection(
            name="health_tips",
            embedding_function=self.embedding_function
        )
        self.products = self.client.get_or_create_collection(
            name="products",
            embedding_function=self.embedding_function
        )
        self.chat_history = self.client.get_or_create_collection(
            name="chat_history",
            embedding_function=self.embedding_function
        )
        self.feedback = self.client.get_or_create_collection(
            name="feedback",
            embedding_function=self.embedding_function
        )
        self.user_profiles = self.client.get_or_create_collection(
            name="user_profiles",
            embedding_function=self.embedding_function
        )

        # Initialize with default data
        self._initialize_default_data()

    def _initialize_default_data(self):
        """Initialize collections with default data if empty"""
        try:
            # Initialize default health tips
            if len(self.health_tips.get()['ids']) == 0:
                default_tips = [
                    {
                        "id": "tip1",
                        "text": "Aim for 7-9 hours of sleep each night for optimal health.",
                        "category": "sleep"
                    },
                    {
                        "id": "tip2",
                        "text": "Stay hydrated by drinking at least 8 glasses of water daily.",
                        "category": "general"
                    },
                    {
                        "id": "tip3",
                        "text": "Regular exercise can improve both physical and mental health.",
                        "category": "lifestyle"
                    }
                ]
                
                for tip in default_tips:
                    self.health_tips.add(
                        documents=[tip["text"]],
                        metadatas=[{"category": tip["category"]}],
                        ids=[tip["id"]]
                    )

            # Initialize default products
            if len(self.products.get()['ids']) == 0:
                default_products = [
                    {
                        "id": "prod1",
                        "name": "Sleep Support Supplement",
                        "description": "Natural supplement with Melatonin and Magnesium for better sleep.",
                        "category": "sleep",
                        "price": 29.99
                    },
                    {
                        "id": "prod2",
                        "name": "Stress Relief Tea",
                        "description": "Herbal tea blend for relaxation and better sleep.",
                        "category": "general",
                        "price": 15.99
                    },
                    {
                        "id": "prod3",
                        "name": "Multivitamin Complex",
                        "description": "Complete daily vitamin and mineral supplement.",
                        "category": "general",
                        "price": 24.99
                    }
                ]
                
                for product in default_products:
                    self.products.add(
                        documents=[product["description"]],
                        metadatas=[{
                            "name": product["name"],
                            "category": product["category"],
                            "price": product["price"]
                        }],
                        ids=[product["id"]]
                    )
                
        except Exception as e:
            print(f"Error initializing default data: {str(e)}")

    def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """Get user profile from database"""
        try:
            results = self.user_profiles.get(
                where={"user_id": user_id},
                limit=1
            )
            
            if results and results['metadatas']:
                return results['metadatas'][0]
            return None
            
        except Exception as e:
            print(f"Error getting user profile: {str(e)}")
            return None

    def store_user_profile(self, user_id: str, profile: Dict) -> bool:
        """Store user profile in database"""
        try:
            # Convert profile to string for document
            profile_str = f"User Profile for {user_id}"
            
            # Store profile
            self.user_profiles.upsert(
                documents=[profile_str],
                metadatas=[profile],
                ids=[f"profile_{user_id}"]
            )
            return True
            
        except Exception as e:
            print(f"Error storing user profile: {str(e)}")
            return False

    def get_relevant_content(self, query: str, user_profile: Optional[Dict] = None, limit: int = 5) -> Dict:
        """Get relevant content based on query using vector similarity"""
        try:
            print(f"\n=== Getting Relevant Content for Query: {query} ===")
            
            # Use user profile topics to enhance search if available
            search_query = query
            if user_profile and user_profile.get('key_topics'):
                topics = ' '.join(user_profile['key_topics'])
                search_query = f"{query} {topics}"
            
            # Get relevant health tips
            health_results = self.health_tips.query(
                query_texts=[search_query],
                n_results=min(limit, len(self.health_tips.get()['ids']))
            )
            
            # Get relevant products
            product_results = self.products.query(
                query_texts=[search_query],
                n_results=min(limit, len(self.products.get()['ids']))
            )
            
            print(f"Found {len(health_results['documents'][0] if health_results['documents'] else [])} relevant health tips")
            print(f"Found {len(product_results['documents'][0] if product_results['documents'] else [])} relevant products")
            
            return {
                'health_tips': {
                    'documents': health_results['documents'][0] if health_results['documents'] else [],
                    'metadatas': health_results['metadatas'][0] if health_results['metadatas'] else []
                },
                'products': {
                    'documents': product_results['documents'][0] if product_results['documents'] else [],
                    'metadatas': product_results['metadatas'][0] if product_results['metadatas'] else []
                }
            }
            
        except Exception as e:
            print(f"Error getting relevant content: {str(e)}")
            return {
                'health_tips': {'documents': [], 'metadatas': []}, 
                'products': {'documents': [], 'metadatas': []}
            }

    def get_health_tips(self, category: Optional[str] = None, limit: int = 5) -> Dict:
        """Get health tips with proper error handling"""
        try:
            if category:
                results = self.health_tips.query(
                    query_texts=["health tips"],
                    where={"category": category},
                    n_results=min(limit, len(self.health_tips.get()['ids']))
                )
            else:
                results = self.health_tips.query(
                    query_texts=["health tips"],
                    n_results=min(limit, len(self.health_tips.get()['ids']))
                )
            
            return {
                'documents': results['documents'][0] if results['documents'] else [],
                'metadatas': results['metadatas'][0] if results['metadatas'] else []
            }
            
        except Exception as e:
            print(f"Error getting health tips: {str(e)}")
            return {'documents': [], 'metadatas': []}

    def get_products_by_category(self, category: str) -> Dict:
        """Get products by category with proper error handling"""
        try:
            results = self.products.query(
                query_texts=[""],
                where={"category": category},
                n_results=min(5, len(self.products.get()['ids']))
            )
            
            return {
                'documents': results['documents'][0] if results['documents'] else [],
                'metadatas': results['metadatas'][0] if results['metadatas'] else []
            }
            
        except Exception as e:
            print(f"Error getting products: {str(e)}")
            return {'documents': [], 'metadatas': []}

    def store_chat(self, user_id: str, message: str, response: str) -> bool:
        """Store chat with proper error handling"""
        try:
            chat_id = f"chat_{user_id}_{datetime.now().timestamp()}"
            self.chat_history.add(
                documents=[f"User: {message}\nBot: {response}"],
                metadatas=[{
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat()
                }],
                ids=[chat_id]
            )
            return True
        except Exception as e:
            print(f"Error storing chat: {str(e)}")
            return False

    def store_feedback(self, user_id: str, rating: int, comment: str) -> bool:
        """Store user feedback"""
        try:
            feedback_id = f"feedback_{user_id}_{datetime.now().timestamp()}"
            self.feedback.add(
                documents=[comment],
                metadatas=[{
                    "user_id": user_id,
                    "rating": rating,
                    "timestamp": datetime.now().isoformat()
                }],
                ids=[feedback_id]
            )
            return True
        except Exception as e:
            print(f"Error storing feedback: {str(e)}")
            return False

    def get_chat_history(self, user_id: str, limit: int = 10) -> Dict:
        """Get chat history with proper error handling"""
        try:
            results = self.chat_history.query(
                query_texts=[""],
                where={"user_id": user_id},
                n_results=min(limit, len(self.chat_history.get()['ids']))
            )
            
            return {
                'documents': results['documents'][0] if results['documents'] else [],
                'metadatas': results['metadatas'][0] if results['metadatas'] else []
            }
            
        except Exception as e:
            print(f"Error getting chat history: {str(e)}")
            return {'documents': [], 'metadatas': []}
        


"""
ChromaDBManager: Core Database Management System for Health Chatbot

This class manages all database operations using ChromaDB, a vector database that enables 
semantic search capabilities. It handles five main collections:

1. health_tips: Stores health-related tips and advice
2. products: Stores product information and descriptions
3. chat_history: Stores user conversations
4. feedback: Stores user feedback and ratings
5. user_profiles: Stores user information and preferences

Key Features:
- Vector embeddings for semantic search
- Automatic data persistence
- Default data initialization
- Error handling for all operations
- User profile management
- Context-aware content retrieval

Collections Structure:
1. health_tips:
   - documents: tip text
   - metadata: category
   - ids: unique tip identifier

2. products:
   - documents: product descriptions
   - metadata: name, category, price
   - ids: unique product identifier

3. chat_history:
   - documents: conversation text
   - metadata: user_id, timestamp
   - ids: unique chat identifier

4. feedback:
   - documents: feedback comments
   - metadata: user_id, rating, timestamp
   - ids: unique feedback identifier

5. user_profiles:
   - documents: profile summary
   - metadata: user preferences and history
   - ids: unique profile identifier

Main Methods:
- get_user_profile(): Retrieves user profile information
- store_user_profile(): Stores or updates user profiles
- get_relevant_content(): Performs semantic search for relevant content
- get_health_tips(): Retrieves health tips by category
- get_products_by_category(): Retrieves products by category
- store_chat(): Stores chat interactions
- store_feedback(): Stores user feedback
- get_chat_history(): Retrieves chat history

Error Handling:
- All methods include try-except blocks
- Failed operations return empty results or False
- Errors are logged for debugging

Vector Search:
- Uses DefaultEmbeddingFunction for text vectorization
- Enables semantic similarity search
- Supports context-aware retrievals

Usage:
db_manager = ChromaDBManager(persist_directory)
db_manager.get_relevant_content(query, user_profile)
"""