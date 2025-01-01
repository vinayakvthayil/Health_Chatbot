# backend/services/health_tips.py
from typing import Dict, List, Optional
import random

class HealthTipsService:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.categories = ['sleep', 'sexual_health', 'general_health', 'lifestyle']
        
        # Default tips in case database is empty
        self.default_tips = [
            {
                "tip": "Maintain a regular sleep schedule",
                "category": "sleep"
            },
            {
                "tip": "Stay hydrated throughout the day",
                "category": "general_health"
            },
            {
                "tip": "Exercise regularly for better health",
                "category": "lifestyle"
            }
        ]
    
    def get_random_tip(self, category: Optional[str] = None) -> Dict:
        """Get a random health tip, optionally filtered by category"""
        try:
            # Get tips from database
            results = self.db_manager.get_health_tips(
                category=category,
                limit=5
            )
            
            # Check if we got any results
            if results and results.get('documents') and len(results['documents']) > 0:
                # Safely get a random index
                index = random.randint(0, len(results['documents']) - 1)
                
                return {
                    "tip": results['documents'][index],
                    "category": results['metadatas'][index]['category'],
                    "related_products": self.get_related_products(results['metadatas'][index]['category'])
                }
            else:
                # If no results from database, use default tips
                default_tip = random.choice(self.default_tips)
                return {
                    "tip": default_tip["tip"],
                    "category": default_tip["category"],
                    "related_products": []
                }
                
        except Exception as e:
            print(f"Error getting random tip: {str(e)}")
            # Return a safe default response
            return {
                "tip": "Remember to maintain a healthy lifestyle!",
                "category": "general_health",
                "related_products": []
            }
    
    def get_related_products(self, category: str) -> List[Dict]:
        """Get products related to a specific health category"""
        try:
            results = self.db_manager.get_products_by_category(category)
            
            if results and results.get('documents'):
                return [{
                    "name": metadata.get('name', 'Unknown Product'),
                    "description": doc,
                    "price": metadata.get('price', 0.0)
                } for doc, metadata in zip(results['documents'], results['metadatas'])]
            return []
            
        except Exception as e:
            print(f"Error getting related products: {str(e)}")
            return []
        


"""
HealthTipsService: Health Tips and Product Recommendation System

This class manages the generation and delivery of health tips and related product
recommendations, supporting both database-sourced and default tips when needed.

Key Features:
1. Tip Management:
   - Random tip selection
   - Category filtering
   - Default tip fallback
   - Product linking

2. Categories:
   - Sleep
   - Sexual Health
   - General Health
   - Lifestyle

Data Structures:
1. Tips Format:
{
    "tip": "tip_text",
    "category": "category_name",
    "related_products": [
        {
            "name": "product_name",
            "description": "product_description",
            "price": price_value
        }
    ]
}

2. Default Tips:
- Maintained in memory
- Basic health advice
- Category-tagged
- Fallback system

Features:
1. Random Tip Generation:
   - Database query
   - Random selection
   - Category filtering
   - Default fallback

2. Product Linking:
   - Category-based matching
   - Product details
   - Price information
   - Description inclusion

Error Handling:
- Database errors
- Empty results
- Category mismatches
- Safe defaults

Usage Example:
service = HealthTipsService(db_manager)
tip = service.get_random_tip(category='sleep')

Note: This service implements the Initial Engagement
requirement from the MVP, providing health tips and
product recommendations.
"""