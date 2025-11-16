from typing import Dict
import openai
import os

class AICoach:
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.openai_api_key
    
    async def generate_daily_plan(self, user_id: int) -> Dict:
        user_progress = await self.get_user_progress(user_id)
        
        prompt = f"""
        Create a daily learning plan for a student with:
        - English level: {user_progress.subjects['english']['level']}
        - Math level: {user_progress.subjects['math']['level']}
        - Programming level: {user_progress.subjects['programming']['level']}
        - Weak topics: {user_progress.weak_topics}
        
        Generate a balanced 30-minute study plan.
        """
        
        # This would call OpenAI API
        response = await self.call_ai(prompt)
        
        return {
            "goals": "• Review 10 vocabulary words\n• Complete 5 math problems\n• Practice pronunciation",
            "subjects": "• English (15 mins)\n• Math (10 mins)\n• Programming (5 mins)",
            "estimated_time": 30
        }
    
    async def answer_question(self, user_id: int, question: str) -> str:
        prompt = f"""
        Answer this student's question in a helpful, educational way:
        Question: {question}
        
        Provide a clear explanation and maybe a follow-up question to check understanding.
        """
        
        # Call AI API
        return "Great question! Here's the explanation..."
    
    async def call_ai(self, prompt: str) -> str:
        # Implement AI API call
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except:
            return "I'm here to help you learn! Let me think about that..."
