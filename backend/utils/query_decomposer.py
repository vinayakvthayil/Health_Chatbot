# backend/utils/query_decomposer.py
import google.generativeai as genai
from typing import List, Dict
import json

class QueryDecomposer:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config={
                "temperature": 0.3,
                "top_p": 0.8,
                "top_k": 20,
                "max_output_tokens": 1024,
            }
        )
        
    def decompose_query(self, query: str) -> Dict[str, List[str]]:
        """Decompose main query into sub-queries and determine search necessity"""
        prompt = f"""Analyze the following health-related query and:
1. Determine if we need to search for scientific research (yes/no)
2. Decompose into 3-4 specific sub-queries if research is needed

Query: {query}

Provide response in the following JSON format:
{{
    "needs_research": true/false,
    "sub_queries": [
        "What is [topic] and its basic mechanisms?",
        "What are the proven benefits of [topic]?",
        "What are the potential risks and side effects of [topic]?",
        "What does recent scientific research say about [topic]'s safety?"
    ]
}}

If research is not needed, return empty sub_queries list.
"""

        try:
            print(f"\n=== Decomposing Query: {query} ===")
            response = self.model.generate_content(prompt)
            
            # Parse JSON response
            result = json.loads(response.text)
            print(f"Needs Research: {result['needs_research']}")
            if result['needs_research']:
                print("Sub-queries:", result['sub_queries'])
            
            return result
            
        except Exception as e:
            print(f"Error decomposing query: {str(e)}")
            return {
                "needs_research": False,
                "sub_queries": []
            }
        


"""
QueryDecomposer: Query Analysis and Decomposition System for Health Chatbot

This class uses Gemini Flash model to analyze user queries and break them down into
sub-queries when detailed research is needed. It's the first step in the chatbot's
processing pipeline, determining how to handle each user query.

Key Features:
1. Query Analysis:
   - Determines if scientific research is needed
   - Breaks complex queries into simpler sub-queries
   - Uses low temperature for consistent outputs

2. Model Configuration:
   - Uses Gemini Flash for fast processing
   - Conservative temperature (0.3) for focused outputs
   - Limited token output for efficiency
   - Optimized top_p and top_k for reliable results

Output Structure:
{
    "needs_research": boolean,  # Whether query needs research
    "sub_queries": [           # List of sub-queries if research needed
        "What is [topic]...?",
        "What are benefits...?",
        "What are risks...?",
        "What does research say...?"
    ]
}

Decomposition Strategy:
1. Basic Understanding: What is the topic/mechanism?
2. Benefits Analysis: What are proven benefits?
3. Risk Assessment: What are potential risks?
4. Research Validation: What does science say?

Error Handling:
- Returns safe default values on errors
- Logs decomposition process
- Maintains service continuity

Usage Example:
decomposer = QueryDecomposer(api_key)
result = decomposer.decompose_query("Is ashwagandha safe?")
# Returns:
# {
#     "needs_research": true,
#     "sub_queries": [
#         "What is ashwagandha and how does it work?",
#         "What are the proven benefits of ashwagandha?",
#         "What are the potential risks of ashwagandha?",
#         "What does research say about ashwagandha safety?"
#     ]
# }

Note: This component is crucial for determining when to activate
the research pipeline and how to structure the information gathering
process.
"""