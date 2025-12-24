import asyncio
import json
import litellm
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

litellm.set_verbose = False

async def get_best_response(query: str) -> Dict[str, Any]:
    """Query both LLMs in parallel and use judge to determine best response"""
    
    # Parallel calls to both LLMs
    gemini_task = litellm.acompletion(
        model="gemini/gemini-1.5-flash",
        messages=[{"role": "user", "content": query}],
        api_key=os.getenv("GEMINI_API_KEY")
    )
    
    openai_task = litellm.acompletion(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}],
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    try:
        gemini_resp, openai_resp = await asyncio.gather(gemini_task, openai_task)
        
        gemini_content = gemini_resp.choices[0].message.content
        openai_content = openai_resp.choices[0].message.content
        
        # Judge prompt
        judge_prompt = f"""Query: {query}

Response A (Gemini): {gemini_content}

Response B (OpenAI): {openai_content}

Analyze both responses and pick the BEST one (A, B, or tie). Consider accuracy, completeness, and relevance. Explain your reasoning in one clear sentence.

Return ONLY valid JSON in this exact format:
{{"winner": "A", "reason": "explanation here", "confidence": 0.95}}

Winner must be exactly "A", "B", or "tie". Confidence must be between 0.0 and 1.0."""

        judge_resp = await litellm.acompletion(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": judge_prompt}],
            api_key=os.getenv("OPENAI_API_KEY")
        )
        
        judge_content = judge_resp.choices[0].message.content.strip()
        
        # Parse judge response
        try:
            judge_data = json.loads(judge_content)
            winner = judge_data.get("winner", "tie")
            reason = judge_data.get("reason", "No reason provided")
            confidence = float(judge_data.get("confidence", 0.5))
        except (json.JSONDecodeError, ValueError):
            winner = "tie"
            reason = "Judge response parsing failed"
            confidence = 0.5
        
        # Determine winner and loser responses
        if winner == "A":
            winner_response = gemini_content
            loser_response = openai_content
        elif winner == "B":
            winner_response = openai_content
            loser_response = gemini_content
        else:
            winner_response = gemini_content  # Default to Gemini for ties
            loser_response = openai_content
        
        return {
            "winner": winner,
            "winner_response": winner_response,
            "loser_response": loser_response,
            "judge_reason": reason,
            "confidence": confidence,
            "gemini_response": gemini_content,
            "openai_response": openai_content
        }
        
    except Exception as e:
        # Fallback response
        return {
            "winner": "error",
            "winner_response": f"Error occurred: {str(e)}",
            "loser_response": "Service unavailable",
            "judge_reason": "API error occurred",
            "confidence": 0.0,
            "gemini_response": f"Error: {str(e)}",
            "openai_response": f"Error: {str(e)}"
        }