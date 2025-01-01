# backend/utils/response_generator.py
import google.generativeai as genai
from typing import Dict, List, Optional

class ResponseGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config={
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
            }
        )
    
    async def generate_response(
        self, 
        original_query: str, 
        sub_queries: List[str], 
        research_results: Dict[str, str],
        rag_context: Optional[str] = None,
        user_profile: Optional[Dict] = None
    ) -> str:
        """Generate natural, contextual response using Chain of Thought"""
        try:
            print("\n=== Generating Response ===")
            
            # Prepare context information
            context_parts = []
            
            # Add RAG context if available
            if rag_context:
                context_parts.append(f"Local Knowledge:\n{rag_context}")
            
            # Add user profile context if available
            if user_profile and user_profile.get('summary'):
                context_parts.append(f"User Context:\n{user_profile['summary']}")
            
            # Add research findings
            if research_results:
                research_summary = "\n".join([
                    f"Research on {query}:\n{results}"
                    for query, results in research_results.items()
                ])
                context_parts.append(f"Research Findings:\n{research_summary}")
            
            # Combine all context
            context = "\n\n".join(context_parts)
            
            prompt = f"""As a health advisor, use Chain of Thought reasoning to provide a helpful response.

User Query: {original_query}

Context Information:
{context}

Think through these steps:

1. Query Analysis:
- What is the main health topic/concern?
- Is this a general or specific question?
- What level of detail is appropriate?

2. Context Evaluation:
- What relevant information do we have?
- Are there any safety concerns?
- What research findings are most relevant?

3. Response Planning:
- What key points should be addressed?
- Are there any warnings needed?
- Should we recommend professional consultation?

4. Response Formulation:
- Start with direct answer
- Include relevant context naturally
- Add safety information if needed
- Suggest professional help if appropriate

Important Guidelines:
- Only mention general health tips (water, sleep, vitamins) if directly relevant
- Include product recommendations only if specifically relevant
- Keep the response focused on the user's question
- Be clear about limitations and uncertainties
- Maintain a conversational but professional tone

Now, think through your response step by step, then provide a natural, focused answer that addresses the user's specific question.

Reasoning:"""

            print("Getting CoT response from Gemini...")
            cot_response = self.model.generate_content(prompt)
            
            # Generate final response without the reasoning
            final_prompt = f"""Based on this reasoning:

{cot_response.text}

Generate a natural, conversational response that focuses specifically on answering the user's question:
"{original_query}"

Remember:
- Be direct and relevant
- Don't force general health tips
- Only mention products if truly relevant
- Keep it concise and natural

Final Response:"""

            final_response = self.model.generate_content(final_prompt)
            print("Response generated successfully")
            
            return final_response.text
            
        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return """I apologize, but I'm having trouble generating a response right now. 
For your safety and best advice, please consider consulting with a healthcare professional."""









"""
ResponseGenerator: Advanced Response Generation System for Health Chatbot

This class manages the generation of comprehensive, context-aware responses using
Gemini Pro model. It implements Chain of Thought (CoT) reasoning for more accurate
and relevant responses to health-related queries.

Key Features:
1. Two-Stage Generation:
   - Chain of Thought reasoning stage
   - Natural response formulation stage
   
2. Context Integration:
   - Local knowledge (RAG)
   - User profile information
   - Research findings
   - Previous conversation context

3. Response Guidelines:
   - Relevance-based health tips
   - Contextual product recommendations
   - Safety-first approach
   - Professional consultation suggestions

Model Configuration:
- Uses Gemini-1.5-Pro
- Balanced temperature (0.7) for creativity
- High top_p (0.95) for natural variation
- Large output capacity (8192 tokens)

Process Flow:
1. Context Preparation:
   - Combines RAG context
   - Integrates user profile
   - Incorporates research findings

2. Chain of Thought:
   - Query analysis
   - Context evaluation
   - Response planning
   - Safety consideration

3. Final Response:
   - Natural language generation
   - Focus on relevance
   - Safety warnings when needed
   - Professional recommendations

Error Handling:
- Comprehensive exception management
- Safe default responses
- Detailed error logging

Usage Example:
generator = ResponseGenerator(api_key)
response = await generator.generate_response(
    query="Is melatonin safe?",
    sub_queries=["safety", "dosage"],
    research_results={"safety": "Studies show..."},
    rag_context="Local data about melatonin..."
)

Note: This component ensures responses are:
- Scientifically accurate
- Contextually relevant
- Safety-conscious
- Natural and helpful
"""