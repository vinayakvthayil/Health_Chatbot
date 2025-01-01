import json
import os
from chromadb_manager import ChromaDBManager

def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def init_database():
    # Get the absolute path to the data directory
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    data_dir = os.path.join(base_dir, 'data')
    chroma_dir = os.path.join(data_dir, 'chromadb')
    
    # Create ChromaDB manager
    db_manager = ChromaDBManager(chroma_dir)
    
    # Load and insert health tips
    tips_data = load_json_data(os.path.join(data_dir, 'health_knowledge', 'health_tips.json'))
    for tip in tips_data['tips']:
        db_manager.add_health_tip(
            tip_id=tip['id'],
            tip_text=tip['text'],
            category=tip['category']
        )
    
    # Load and insert FAQs
    faqs_data = load_json_data(os.path.join(data_dir, 'health_knowledge', 'faqs.json'))
    for faq in faqs_data['faqs']:
        db_manager.add_faq(
            faq_id=faq['id'],
            question=faq['question'],
            answer=faq['answer'],
            category=faq['category']
        )
    
    # Load and insert products
    products_data = load_json_data(os.path.join(data_dir, 'health_knowledge', 'products.json'))
    for product in products_data['products']:
        db_manager.add_product(
            product_id=product['id'],
            name=product['name'],
            description=product['description'],
            category=product['category'],
            price=product['price']
        )

if __name__ == "__main__":
    init_database()
    print("Database initialized successfully!")










    """
Database Initialization Script for Health Chatbot

This script initializes the ChromaDB database with default data from JSON files.
It serves as a setup tool to populate the database with initial health tips,
FAQs, and product information.

File Structure Required:
data/
├── health_knowledge/
│   ├── health_tips.json
│   ├── faqs.json
│   └── products.json
└── chromadb/

JSON File Formats:

1. health_tips.json:
{
    "tips": [
        {
            "id": "unique_id",
            "text": "tip content",
            "category": "category_name"
        }
    ]
}

2. faqs.json:
{
    "faqs": [
        {
            "id": "unique_id",
            "question": "question text",
            "answer": "answer text",
            "category": "category_name"
        }
    ]
}

3. products.json:
{
    "products": [
        {
            "id": "unique_id",
            "name": "product name",
            "description": "product description",
            "category": "category_name",
            "price": float_value
        }
    ]
}

Functions:
- load_json_data(): Loads and parses JSON files
- init_database(): Main initialization function that:
  1. Sets up ChromaDB manager
  2. Loads JSON data
  3. Populates database collections

Usage:
python init_db.py

Note: This script should be run once during initial setup or when
resetting the database with default data.
"""