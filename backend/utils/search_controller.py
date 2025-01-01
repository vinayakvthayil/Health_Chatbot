# backend/utils/search_controller.py
from openai import AsyncOpenAI
from typing import List, Dict
import json
import asyncio

class SearchController:
    def __init__(self, api_key: str):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "llama-3.1-sonar-small-128k-online"
    
    async def search_research(self, queries: List[str]) -> Dict[str, str]:
        """Search for research papers and medical data"""
        results = {}
        
        # Process queries concurrently
        async def process_query(query: str) -> tuple:
            try:
                print(f"\n=== Searching for: {query} ===")
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": """You are a medical research assistant. Search and summarize recent, reliable research papers and medical data.
Focus on:
1. Scientific evidence and clinical studies
2. Potential health risks and safety concerns
3. Expert medical opinions
4. Recent research findings

Format your response to include:
- Key findings
- Safety warnings
- Scientific consensus
- References to studies (if available)"""
                        },
                        {
                            "role": "user",
                            "content": f"Search for recent scientific research about: {query}"
                        }
                    ],
                    temperature=0.3,
                    max_tokens=1024
                )
                
                content = response.choices[0].message.content
                print(f"Found research for: {query}")
                return query, content
                
            except Exception as e:
                print(f"Error searching for {query}: {str(e)}")
                return query, f"Error retrieving research: {str(e)}"
        
        # Process all queries concurrently
        tasks = [process_query(query) for query in queries]
        query_results = await asyncio.gather(*tasks)
        
        # Convert results to dictionary
        results = dict(query_results)
        
        return results
    


"""
SearchController: Research and Medical Data Search System

This class manages concurrent searches for medical research and data using
Perplexity's Sonar model. It processes multiple research queries simultaneously
for efficient information gathering.

Key Features:
1. Concurrent Processing:
   - Asynchronous query handling
   - Parallel research searches
   - Efficient resource utilization

2. Research Focus:
   - Scientific evidence
   - Clinical studies
   - Safety concerns
   - Expert opinions

3. Response Formatting:
   - Key findings
   - Safety warnings
   - Scientific consensus
   - Study references

Model Configuration:
- Uses llama-3.1-sonar-small-128k-online
- Low temperature (0.3) for accuracy
- Controlled token output (1024)
- Research-focused system prompt

Process Flow:
1. Query Reception:
   - Takes list of research queries
   - Prepares concurrent tasks

2. Parallel Processing:
   - Creates async tasks for each query
   - Manages concurrent execution
   - Handles individual query failures

3. Result Aggregation:
   - Combines all search results
   - Maintains query-result mapping
   - Handles errors gracefully

Error Handling:
- Per-query error management
- Graceful failure handling
- Detailed error reporting

Usage Example:
controller = SearchController(api_key)
results = await controller.search_research([
    "melatonin safety studies",
    "melatonin dosage research"
])

Note: This component ensures:
- Efficient research gathering
- Reliable scientific information
- Comprehensive error handling
- Structured research results
"""