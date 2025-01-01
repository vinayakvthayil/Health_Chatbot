# backend/utils/rag_handler.py
from typing import Dict, List, Optional

class RAGHandler:
    def __init__(self, db_manager):
        self.db_manager = db_manager
    
    def get_relevant_context(
        self, 
        query: str,
        user_profile: Optional[Dict] = None
    ) -> str:
        """Get relevant context from database"""
        try:
            print("\n=== RAG Debug: Starting Context Retrieval ===")
            print(f"User Query: {query}")
            
            # Get relevant content using user profile
            relevant_content = self.db_manager.get_relevant_content(
                query=query,
                user_profile=user_profile
            )
            
            # Extract health tips and products
            health_tips = relevant_content['health_tips']
            products = relevant_content['products']
            
            print("\nRetrieved Health Tips:")
            for tip in health_tips['documents']:
                print(f"- {tip}")
            
            print("\nRetrieved Products:")
            for doc, meta in zip(products['documents'], products['metadatas']):
                print(f"- {meta.get('name', 'Unknown')}: {doc}")
            
            # Combine context
            context_parts = []
            
            # Add health tips to context
            if health_tips['documents']:
                tips_context = "\n".join([
                    f"Health Tip: {tip}" 
                    for tip in health_tips['documents']
                ])
                context_parts.append(tips_context)
            
            # Add products to context
            if products['documents']:
                products_context = "\n".join([
                    f"Product: {meta.get('name', 'Unknown')} - {doc}"
                    for doc, meta in zip(products['documents'], products['metadatas'])
                ])
                context_parts.append(products_context)
            
            # Add user context if available
            if user_profile and user_profile.get('summary'):
                context_parts.append(f"User History: {user_profile['summary']}")
            
            final_context = "\n\n".join(context_parts)
            
            print("\nFinal Combined Context:")
            print(final_context)
            print("\n=== RAG Debug: Context Retrieval Complete ===")
            
            return final_context
            
        except Exception as e:
            print(f"\nError getting context: {str(e)}")
            return ""
        


"""
RAGHandler: Retrieval-Augmented Generation Handler for Health Chatbot

This class manages the retrieval of relevant context from the database to enhance
the chatbot's responses with local knowledge. It combines health tips, product
information, and user history to provide context-aware responses.

Key Features:
1. Context Retrieval:
   - Fetches relevant health tips
   - Retrieves related products
   - Incorporates user history
   - Combines multiple context sources

2. User Profile Integration:
   - Uses user profile for context enhancement
   - Personalizes content retrieval
   - Maintains user history context

Context Components:
1. Health Tips:
   - Relevant health advice
   - Category-specific information
   - General wellness guidelines

2. Products:
   - Related product information
   - Product descriptions
   - Pricing and categories

3. User History:
   - Previous interactions
   - User preferences
   - Historical context

Output Format:
- Structured text combining:
  * Health tips
  * Product information
  * User history
- Formatted for LLM consumption
- Debug information for monitoring

Debug Features:
- Detailed logging of retrieval process
- Context composition tracking
- Error reporting and handling

Usage Example:
rag_handler = RAGHandler(db_manager)
context = rag_handler.get_relevant_context(
    query="sleep issues",
    user_profile={"summary": "Previous sleep-related queries"}
)

Error Handling:
- Returns empty string on errors
- Logs all retrieval steps
- Maintains system stability

Note: This component is essential for providing relevant context
to the LLM, improving response accuracy and personalization.
"""