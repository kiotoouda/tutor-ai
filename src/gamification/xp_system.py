import math
from datetime import datetime, timedelta
from typing import Dict, List

class XPSystem:
    def __init__(self):
        self.xp_requirements = [0, 100, 300, 600, 1000, 1500, 2100, 2800, 3600, 4500]
        self.exercise_xp = {
            "easy": 10,
            "medium": 25,
            "hard": 50,
            "perfect_lesson": 15,
            "streak_bonus": 5,
            "photo_solve": 25,
            "speaking_practice": 15,
            "coding_challenge": 30
        }
    
    async def add_xp(self, user_id: int, xp: int, activity_type: str):
        # Add XP to user's total and subject-specific XP
        streak_bonus = await self.calculate_streak_bonus(user_id)
        total_xp = xp + streak_bonus
        
        # Update user stats
        # Update subject progress
        # Check for level up
        
        return total_xp
    
    async def calculate_streak_bonus(self, user_id: int) -> int:
        # Calculate bonus based on current streak
        user_stats = await self.get_user_stats(user_id)
        streak = user_stats.current_streak
        
        if streak >= 7:
            return 10
        elif streak >= 30:
            return 25
        elif streak >= 100:
            return 50
        return 0
    
    async def check_level_up(self, user_id: int, subject: str = None) -> Dict:
        # Check if user leveled up
        user_progress = await self.get_user_progress(user_id)
        
        if subject:
            current_xp = user_progress.subjects[subject]["xp"]
            current_level = user_progress.subjects[subject]["level"]
            new_level = self.calculate_level(current_xp)
            
            if new_level > current_level:
                return {
                    "leveled_up": True,
                    "old_level": current_level,
                    "new_level": new_level,
                    "subject": subject
                }
        
        return {"leveled_up": False}
    
    def calculate_level(self, xp: int) -> int:
        level = 1
        for i, requirement in enumerate(self.xp_requirements[1:], 1):
            if xp >= requirement:
                level = i + 1
            else:
                break
        return level
    
    async def get_user_profile(self, user_id: int) -> Dict:
        user = await self.get_user(user_id)
        stats = await self.get_user_stats(user_id)
        progress = await self.get_user_progress(user_id)
        
        return {
            "username": user.username,
            "global_level": stats.global_level,
            "english_level": progress.subjects["english"]["level"],
            "math_level": progress.subjects["math"]["level"],
            "programming_level": progress.subjects["programming"]["level"],
            "total_xp": stats.total_xp,
            "current_streak": stats.current_streak,
            "longest_streak": stats.longest_streak,
            "learning_time": stats.total_learning_time,
            "vocabulary_size": progress.subjects["english"]["vocabulary_size"],
            "mastery_percentage": self.calculate_mastery(progress),
            "completed_units": self.count_completed_units(progress)
        }
    
    def calculate_mastery(self, progress) -> float:
        # Calculate overall mastery percentage
        total_mastery = sum(
            subject["mastery_percentage"] 
            for subject in progress.subjects.values()
        )
        return total_mastery / len(progress.subjects)
    
    def count_completed_units(self, progress) -> int:
        # Count completed units across all subjects
        return sum(
            len(subject.get("completed_lessons", [])) 
            for subject in progress.subjects.values()
        )
