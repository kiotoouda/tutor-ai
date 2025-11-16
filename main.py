import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from src.database.models import User, UserStats, UserProgress
from src.gamification.xp_system import XPSystem
from src.learning.language_mode import LanguageLearning
from src.learning.math_mode import MathLearning
from src.ai.coaching import AICoach

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LearningBot:
    def __init__(self, token: str):
        self.application = Application.builder().token(token).build()
        self.xp_system = XPSystem()
        self.language_learning = LanguageLearning()
        self.math_learning = MathLearning()
        self.ai_coach = AICoach()
        self.setup_handlers()
    
    def setup_handlers(self):
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("profile", self.show_profile))
        self.application.add_handler(CommandHandler("stats", self.show_stats))
        self.application.add_handler(CommandHandler("daily", self.daily_lesson))
        self.application.add_handler(CommandHandler("leaderboard", self.leaderboard))
        
        # Message handlers
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(MessageHandler(filters.PHOTO, self.handle_photo))
        self.application.add_handler(MessageHandler(filters.VOICE, self.handle_voice))
        
        # Callback handlers
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        user_id = user.id
        
        # Initialize user in database
        await self.initialize_user(user_id, user.first_name, user.username)
        
        welcome_text = """
🌟 Welcome to Your AI Learning Companion! 🎓

I'm your personal tutor that will help you master:
• Languages (English, Spanish, French, etc.)
• Math & Physics
• Programming (Python, JavaScript, C++)
• And much more!

📚 Available Commands:
/profile - View your progress
/stats - Detailed statistics
/daily - Get today's lessons
/leaderboard - See rankings
/math - Math exercises
/english - Language practice
/code - Programming challenges

Let's start your learning journey! 🚀
        """
        
        keyboard = [
            [InlineKeyboardButton("🎯 Daily Plan", callback_data="daily_plan")],
            [InlineKeyboardButton("📊 Profile", callback_data="profile")],
            [InlineKeyboardButton("🌍 Language", callback_data="language_mode"),
             InlineKeyboardButton("🔢 Math", callback_data="math_mode")],
            [InlineKeyboardButton("💻 Programming", callback_data="programming_mode")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_text, reply_markup=reply_markup)
    
    async def show_profile(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        profile_data = await self.xp_system.get_user_profile(user_id)
        
        profile_text = f"""
👤 {profile_data['username']}'s Profile

📊 Levels:
• Global Level: {profile_data['global_level']}
• English: Lvl {profile_data['english_level']}
• Math: Lvl {profile_data['math_level']}
• Programming: Lvl {profile_data['programming_level']}

🏆 Stats:
• Total XP: {profile_data['total_xp']:,}
• Current Streak: {profile_data['current_streak']} days 🔥
• Longest Streak: {profile_data['longest_streak']} days
• Learning Time: {profile_data['learning_time']} mins

🎯 Current Progress:
• Vocabulary: {profile_data['vocabulary_size']} words
• Mastery: {profile_data['mastery_percentage']}%
• Completed Units: {profile_data['completed_units']}
        """
        
        await update.message.reply_text(profile_text)
    
    async def daily_lesson(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        daily_plan = await self.ai_coach.generate_daily_plan(user_id)
        
        plan_text = f"""
📅 Your Daily Learning Plan

🎯 Today's Goals:
{daily_plan['goals']}

📚 Subjects:
{daily_plan['subjects']}

⏰ Estimated Time: {daily_plan['estimated_time']} minutes

💪 Let's get started! Complete tasks to earn XP and maintain your streak!
        """
        
        keyboard = [
            [InlineKeyboardButton("Start English Lesson", callback_data="start_english")],
            [InlineKeyboardButton("Start Math Practice", callback_data="start_math")],
            [InlineKeyboardButton("Code Challenge", callback_data="start_coding")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(plan_text, reply_markup=reply_markup)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        message_text = update.message.text
        
        # Check if it's an answer to an exercise
        if await self.is_exercise_response(user_id, message_text):
            await self.check_exercise_answer(user_id, message_text, update)
        else:
            # General AI tutor response
            response = await self.ai_coach.answer_question(user_id, message_text)
            await update.message.reply_text(response)
    
    async def handle_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        photo = update.message.photo[-1]
        
        await update.message.reply_text("📸 Analyzing your problem...")
        
        # This would integrate with OCR and AI solving
        solution = await self.math_learning.solve_photo_problem(photo)
        
        response_text = f"""
✅ Problem Solved!

**Problem:** {solution['problem']}
**Solution:** {solution['solution']}
**Explanation:** {solution['explanation']}

🎯 Practice more similar problems to master this topic!
        """
        
        # Award XP for photo solving
        await self.xp_system.add_xp(user_id, 25, "photo_solve")
        
        await update.message.reply_text(response_text)
    
    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        voice = update.message.voice
        
        await update.message.reply_text("🎤 Analyzing your pronunciation...")
        
        # This would integrate with speech-to-text and pronunciation analysis
        pronunciation_feedback = await self.language_learning.analyze_pronunciation(voice)
        
        feedback_text = f"""
🎯 Pronunciation Analysis:

**You said:** {pronunciation_feedback['transcript']}
**Accuracy:** {pronunciation_feedback['accuracy']}%
**Feedback:** {pronunciation_feedback['feedback']}

💡 Tip: {pronunciation_feedback['tip']}
        """
        
        await update.message.reply_text(feedback_text)
        await self.xp_system.add_xp(user_id, 15, "speaking_practice")

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        
        if callback_data == "daily_plan":
            await self.daily_lesson(update, context)
        elif callback_data == "profile":
            await self.show_profile(update, context)
        elif callback_data == "start_english":
            await self.start_english_lesson(update, context)
        elif callback_data == "start_math":
            await self.start_math_exercise(update, context)
    
    async def start_english_lesson(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        lesson = await self.language_learning.generate_lesson(user_id)
        
        lesson_text = f"""
📚 English Lesson: {lesson['title']}

{lesson['content']}

**Exercise:**
{lesson['exercise']['question']}

Options:
{chr(10).join([f"{chr(65+i)}. {option}" for i, option in enumerate(lesson['exercise']['options'])])}
        """
        
        await context.bot.send_message(chat_id=user_id, text=lesson_text)
    
    async def start_math_exercise(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        exercise = await self.math_learning.generate_exercise(user_id)
        
        exercise_text = f"""
🔢 Math Challenge - {exercise['topic']}

**Problem:**
{exercise['problem']}

Difficulty: {exercise['difficulty']} ⭐
XP Reward: {exercise['xp_reward']}
        """
        
        await context.bot.send_message(chat_id=user_id, text=exercise_text)
    
    async def initialize_user(self, user_id: int, first_name: str, username: str):
        # Initialize user in database
        pass
    
    async def is_exercise_response(self, user_id: int, message: str) -> bool:
        # Check if user is responding to an exercise
        pass
    
    async def check_exercise_answer(self, user_id: int, answer: str, update: Update):
        # Check exercise answer and provide feedback
        pass

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
    
    bot = LearningBot(token)
    
    # Start the bot
    port = int(os.environ.get('PORT', 8443))
    webhook_url = os.getenv("WEBHOOK_URL")
    
    if webhook_url:
        # Production with webhook
        bot.application.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=token,
            webhook_url=f"{webhook_url}/{token}"
        )
    else:
        # Development with polling
        bot.application.run_polling()

if __name__ == "__main__":
    main()
