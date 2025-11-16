import random
import sympy
from typing import Dict

class MathLearning:
    def __init__(self):
        self.topics = {
            "arithmetic": ["addition", "subtraction", "multiplication", "division"],
            "algebra": ["equations", "inequalities", "polynomials"],
            "geometry": ["angles", "triangles", "circles"],
            "calculus": ["derivatives", "integrals"]
        }
    
    async def generate_exercise(self, user_id: int) -> Dict:
        user_progress = await self.get_user_progress(user_id)
        math_level = user_progress.subjects["math"]["level"]
        
        topic = self.select_topic(user_progress)
        problem, solution = self.generate_problem(topic, math_level)
        
        return {
            "topic": topic,
            "problem": problem,
            "solution": solution,
            "difficulty": self.get_difficulty(math_level),
            "xp_reward": math_level * 5
        }
    
    def generate_problem(self, topic: str, level: int) -> tuple:
        if topic == "arithmetic":
            return self.generate_arithmetic_problem(level)
        elif topic == "algebra":
            return self.generate_algebra_problem(level)
        # Add more problem generators...
    
    def generate_arithmetic_problem(self, level: int) -> tuple:
        if level <= 3:
            a, b = random.randint(1, 20), random.randint(1, 20)
            return f"What is {a} + {b}?", str(a + b)
        else:
            a, b, c = random.randint(1, 100), random.randint(1, 100), random.randint(1, 10)
            return f"Calculate: ({a} × {b}) ÷ {c}", str((a * b) // c)
