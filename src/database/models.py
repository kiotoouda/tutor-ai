from typing import Dict, List, Optional
from datetime import datetime, date
import json

class User:
    def __init__(self, user_id: int, username: str, first_name: str):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.created_at = datetime.now()
        self.subscription = "free"  # free, premium
        self.language = "en"
        
class UserStats:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.total_xp = 0
        self.global_level = 1
        self.current_streak = 0
        self.longest_streak = 0
        self.total_learning_time = 0
        self.last_active = datetime.now()
        self.streak_freeze = 0
        
class UserProgress:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.subjects = {
            "english": {
                "level": 1,
                "xp": 0,
                "current_unit": "basics",
                "vocabulary_size": 0,
                "mastery_percentage": 0,
                "completed_lessons": []
            },
            "math": {
                "level": 1,
                "xp": 0,
                "current_topic": "arithmetic",
                "mastery_percentage": 0,
                "completed_exercises": []
            },
            "programming": {
                "level": 1,
                "xp": 0,
                "current_language": "python",
                "mastery_percentage": 0,
                "completed_challenges": []
            }
        }
        self.weak_topics = []
        self.strengths = []
        self.achievements = []
        
class Database:
    def __init__(self):
        self.users = {}
        self.user_stats = {}
        self.user_progress = {}
        self.leaderboards = {}
    
    async def get_user(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)
    
    async def create_user(self, user_id: int, username: str, first_name: str) -> User:
        user = User(user_id, username, first_name)
        self.users[user_id] = user
        self.user_stats[user_id] = UserStats(user_id)
        self.user_progress[user_id] = UserProgress(user_id)
        return user
    
    async def update_user_stats(self, user_id: int, updates: Dict):
        if user_id in self.user_stats:
            for key, value in updates.items():
                setattr(self.user_stats[user_id], key, value)
    
    async def update_user_progress(self, user_id: int, subject: str, updates: Dict):
        if user_id in self.user_progress:
            for key, value in updates.items():
                self.user_progress[user_id].subjects[subject][key] = value
