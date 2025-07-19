import json
import logging
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from eligibility_checker import EligibilityChecker
from recommendation_engine import RecommendationEngine
from utils.validators import Validators
from config import AGE, MAJOR, DEGREE, BACHELOR_FIELD, MASTER_FIELD, GPA, LANGUAGE, BUDGET, COUNTRY, MAJORS, DEGREE_TYPES, BUDGET_RANGES

logger = logging.getLogger(__name__)

class BotHandlers:
    def __init__(self):
        self.eligibility_checker = EligibilityChecker()
        self.recommendation_engine = RecommendationEngine()
        self.validators = Validators()
        
        # Conversation states
        self.AGE = AGE
        self.MAJOR = MAJOR
        self.DEGREE = DEGREE
        self.BACHELOR_FIELD = BACHELOR_FIELD
        self.MASTER_FIELD = MASTER_FIELD
        self.GPA = GPA
        self.LANGUAGE = LANGUAGE
        self.BUDGET = BUDGET
        self.COUNTRY = COUNTRY

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start the conversation and ask for age."""
        user = update.effective_user
        
        welcome_message = f"""
🎓 *به ربات بررسی واجد شرایط بودن برای تحصیل در خارج خوش آمدید!* 🌍

سلام {user.first_name}! من به شما کمک خواهم کرد تا واجد شرایط بودن خود برای تحصیل در خارج از کشور را بررسی کنید و توصیه‌های شخصی‌سازی شده ارائه دهم.

اطلاعاتی که نیاز دارم:
• سن
• رشته تحصیلی فعلی
• مقطع تحصیلی فعلی
• رشته‌های تحصیلی قبلی (در صورت وجود)
• معدل (از ۲۰)
• سطح زبان
• بودجه موجود
• مقصد مورد علاقه برای تحصیل

بیایید شروع کنیم!

📝 *لطفاً سن خود را وارد کنید:*
        """
        
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
        return self.AGE

    async def age(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store age and ask for major."""
        user_input = update.message.text.strip()
        
        if not self.validators.validate_age(user_input):
            await update.message.reply_text(
                "❌ لطفاً یک سن معتبر وارد کنید (عددی بین ۱۶ تا ۸۰):"
            )
            return self.AGE
        
        age = int(user_input)
        context.user_data['age'] = age
        
        # Provide age warning if over 40
        if age > 40:
            await update.message.reply_text(
                "⚠️ *توجه سنی:* شما بالای ۴۰ سال سن دارید. اگرچه این شما را از واجد شرایط بودن خارج نمی‌کند، اما برخی برنامه‌ها ممکن است اولویت را به متقاضیان جوان‌تر بدهند.",
                parse_mode='Markdown'
            )
        
        majors_list = "\n".join([f"• {major}" for major in MAJORS])
        await update.message.reply_text(
            f"📚 *رشته تحصیلی شما چیست؟*\n\nگزینه‌های موجود:\n{majors_list}\n\nلطفاً رشته خود را تایپ کنید:",
            parse_mode='Markdown'
        )
        return self.MAJOR

    async def major(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store major and ask for degree level."""
        user_input = update.message.text.strip()
        
        if not self.validators.validate_major(user_input):
            majors_list = "\n".join([f"• {major}" for major in MAJORS])
            await update.message.reply_text(
                f"❌ لطفاً یک رشته معتبر از لیست انتخاب کنید:\n{majors_list}"
            )
            return self.MAJOR
        
        context.user_data['major'] = user_input
        
        degrees_list = "\n".join([f"• {degree}" for degree in DEGREE_TYPES])
        await update.message.reply_text(
            f"🎓 *مقطع تحصیلی فعلی شما چیست؟*\n\nگزینه‌های موجود:\n{degrees_list}\n\nلطفاً مقطع تحصیلی خود را تایپ کنید:",
            parse_mode='Markdown'
        )
        return self.DEGREE

    async def degree(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store degree and ask for bachelor field if applicable."""
        user_input = update.message.text.strip()
        
        if not self.validators.validate_degree(user_input):
            degrees_list = "\n".join([f"• {degree}" for degree in DEGREE_TYPES])
            await update.message.reply_text(
                f"❌ لطفاً یک مقطع تحصیلی معتبر از لیست انتخاب کنید:\n{degrees_list}"
            )
            return self.DEGREE
        
        context.user_data['degree'] = user_input
        
        # Check associate degree age restriction
        if user_input == 'مدرک فوق دیپلم':
            age = context.user_data.get('age', 0)
            if age >= 23:
                await update.message.reply_text(
                    "❌ *متأسفانه شرایط شما مناسب نیست!*\n\nبرای درخواست مقطع کارشناسی با مدرک فوق دیپلم، باید زیر ۲۳ سال سن داشته باشید.\n\nشما می‌توانید مجدداً بعد از دریافت مدرک کارشناسی اقدام کنید.",
                    parse_mode='Markdown'
                )
                return ConversationHandler.END
        
        # Ask for bachelor field if they have bachelor or higher degrees
        if user_input in ['مدرک کارشناسی', 'مدرک کارشناسی ارشد', 'دکتری']:
            majors_list = "\n".join([f"• {major}" for major in MAJORS])
            await update.message.reply_text(
                f"📚 *رشته تحصیلی در مقطع کارشناسی شما چیست؟*\n\nگزینه‌های موجود:\n{majors_list}\n\nلطفاً رشته کارشناسی خود را تایپ کنید:",
                parse_mode='Markdown'
            )
            return self.BACHELOR_FIELD
        else:
            # Skip field questions for lower degrees
            await update.message.reply_text(
                "📊 *معدل شما از ۲۰ چقدر است؟*\n\nلطفاً عددی بین ۰ تا ۲۰ وارد کنید (مثال: ۱۵.۵):",
                parse_mode='Markdown'
            )
            return self.GPA

    async def bachelor_field(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store bachelor field and ask for master field if applicable."""
        user_input = update.message.text.strip()
        
        if not self.validators.validate_major(user_input):
            majors_list = "\n".join([f"• {major}" for major in MAJORS])
            await update.message.reply_text(
                f"❌ لطفاً یک رشته معتبر از لیست انتخاب کنید:\n{majors_list}"
            )
            return self.BACHELOR_FIELD
        
        context.user_data['bachelor_field'] = user_input
        
        # Ask for master field if they have master's or PhD
        degree = context.user_data.get('degree', '')
        if degree in ['مدرک کارشناسی ارشد', 'دکتری']:
            majors_list = "\n".join([f"• {major}" for major in MAJORS])
            await update.message.reply_text(
                f"📚 *رشته تحصیلی در مقطع کارشناسی ارشد شما چیست؟*\n\nگزینه‌های موجود:\n{majors_list}\n\nلطفاً رشته کارشناسی ارشد خود را تایپ کنید:",
                parse_mode='Markdown'
            )
            return self.MASTER_FIELD
        else:
            # Go to GPA for bachelor's degree
            await update.message.reply_text(
                "📊 *معدل شما از ۲۰ چقدر است؟*\n\nلطفاً عددی بین ۰ تا ۲۰ وارد کنید (مثال: ۱۵.۵):",
                parse_mode='Markdown'
            )
            return self.GPA

    async def master_field(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store master field and ask for GPA."""
        user_input = update.message.text.strip()
        
        if not self.validators.validate_major(user_input):
            majors_list = "\n".join([f"• {major}" for major in MAJORS])
            await update.message.reply_text(
                f"❌ لطفاً یک رشته معتبر از لیست انتخاب کنید:\n{majors_list}"
            )
            return self.MASTER_FIELD
        
        context.user_data['master_field'] = user_input
        
        await update.message.reply_text(
            "📊 *معدل شما از ۲۰ چقدر است؟*\n\nلطفاً عددی بین ۰ تا ۲۰ وارد کنید (مثال: ۱۵.۵):",
            parse_mode='Markdown'
        )
        return self.GPA

    async def gpa(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store GPA and ask for language proficiency."""
        user_input = update.message.text.strip()
        
        if not self.validators.validate_gpa(user_input):
            await update.message.reply_text(
                "❌ لطفاً معدل معتبری بین ۰ تا ۲۰ وارد کنید (مثال: ۱۵.۵):"
            )
            return self.GPA
        
        gpa = float(user_input)
        context.user_data['gpa'] = gpa
        
        # Provide GPA warning if below 13
        if gpa < 13.0:
            await update.message.reply_text(
                "⚠️ *توجه معدل:* معدل شما کمتر از ۱۳ از ۲۰ است. این ممکن است گزینه‌های شما را محدود کند، اما نگران نباشید - هنوز فرصت‌هایی موجود است!",
                parse_mode='Markdown'
            )
        
        await update.message.reply_text(
            """🗣️ *سطح مهارت زبان شما چیست؟*

سطوح موجود:
• A1 - مبتدی
• A2 - ابتدایی
• B1 - متوسط
• B2 - بالاتر از متوسط
• C1 - پیشرفته
• C2 - ماهر

لطفاً سطح خود را تایپ کنید (مثال: B2):""",
            parse_mode='Markdown'
        )
        return self.LANGUAGE

    async def language(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store language level and ask for budget."""
        user_input = update.message.text.strip().upper()
        
        if not self.validators.validate_language_level(user_input):
            await update.message.reply_text(
                "❌ لطفاً سطح زبان معتبری وارد کنید (A1, A2, B1, B2, C1, یا C2):"
            )
            return self.LANGUAGE
        
        context.user_data['language_level'] = user_input
        
        # Provide language warning if below B1
        if user_input in ['A1', 'A2']:
            await update.message.reply_text(
                "⚠️ *توجه زبان:* سطح مهارت شما کمتر از B1 است. اکثر دانشگاه‌ها حداقل سطح B1 را می‌طلبند. توصیه می‌کنیم مهارت زبان خود را بهبود دهید!",
                parse_mode='Markdown'
            )
        
        # Ask for budget
        budget_list = "\n".join([f"• {budget}" for budget in BUDGET_RANGES])
        await update.message.reply_text(
            f"""💰 *بودجه موجود شما برای تحصیل در خارج چقدر است؟*

گزینه‌های موجود:
{budget_list}

لطفاً بودجه خود را انتخاب کنید:""",
            parse_mode='Markdown'
        )
        return self.BUDGET

    async def budget(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store budget and ask for preferred country based on budget."""
        user_input = update.message.text.strip()
        
        if user_input not in BUDGET_RANGES:
            budget_list = "\n".join([f"• {budget}" for budget in BUDGET_RANGES])
            await update.message.reply_text(
                f"❌ لطفاً یک گزینه معتبر از لیست انتخاب کنید:\n{budget_list}"
            )
            return self.BUDGET
        
        context.user_data['budget'] = user_input
        
        # Determine budget category and recommend countries
        from config import BUDGET_COUNTRIES
        if user_input == 'کمتر از ۲ میلیارد تومان':
            recommended_countries = BUDGET_COUNTRIES['low']
            budget_category = 'low'
        elif user_input == 'بین ۲ تا ۳ میلیارد تومان':
            recommended_countries = BUDGET_COUNTRIES['medium']
            budget_category = 'medium'
        else:  # بیشتر از ۳ میلیارد تومان
            recommended_countries = BUDGET_COUNTRIES['high']
            budget_category = 'high'
        
        context.user_data['budget_category'] = budget_category
        
        countries_list = "\n".join([f"• {country}" for country in recommended_countries])
        await update.message.reply_text(
            f"""🌍 *بر اساس بودجه شما، کشورهای زیر توصیه می‌شوند:*

{countries_list}

*کدام کشور را برای تحصیل ترجیح می‌دهید؟*

لطفاً کشور مورد علاقه خود را از لیست بالا تایپ کنید:""",
            parse_mode='Markdown'
        )
        return self.COUNTRY

    async def country(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store country, perform eligibility check, and provide recommendations."""
        user_input = update.message.text.strip()
        context.user_data['preferred_country'] = user_input
        
        # Perform eligibility assessment
        user_data = context.user_data
        eligibility_result = self.eligibility_checker.assess_eligibility(user_data)
        
        # Send eligibility results
        await update.message.reply_text(
            eligibility_result['message'],
            parse_mode='Markdown'
        )
        
        # If eligible, provide recommendations
        if eligibility_result['eligible']:
            recommendations = self.recommendation_engine.get_recommendations(user_data)
            await update.message.reply_text(
                recommendations,
                parse_mode='Markdown'
            )
        else:
            # Provide guidance for improvement
            improvement_tips = self.get_improvement_tips(user_data)
            await update.message.reply_text(
                improvement_tips,
                parse_mode='Markdown'
            )
        
        await update.message.reply_text(
            "✨ *ارزیابی کامل شد!*\n\nاز استفاده شما از ربات بررسی واجد شرایط بودن برای تحصیل در خارج متشکریم. اگر می‌خواهید دوباره شروع کنید، از دستور /start استفاده کنید.",
            parse_mode='Markdown'
        )
        
        return ConversationHandler.END

    def get_improvement_tips(self, user_data):
        """Generate improvement tips for users who don't meet eligibility criteria."""
        tips = ["🎯 *راهنمایی‌هایی برای بهبود واجد شرایط بودن شما:*\n"]
        
        if user_data['gpa'] < 13.0:
            tips.append("📈 *بهبود معدل:* روی درس‌های خود تمرکز کنید تا معدل‌تان را بالای ۱۳ از ۲۰ ببرید. در صورت امکان، دروس را مجدداً بگذرانید.")
        
        if user_data['language_level'] in ['A1', 'A2']:
            tips.append("🗣️ *مهارت‌های زبان:* در کلاس‌های زبان یا برنامه‌های آنلاین ثبت‌نام کنید تا حداقل به سطح B1 برسید. صحبت، گوش دادن، خواندن و نوشتن را تمرین کنید.")
        
        if user_data['age'] > 40:
            tips.append("👥 *در نظر گیری سن:* دنبال دانشگاه‌هایی بگردید که دانشجویان مسن‌تر را می‌پذیرند یا برنامه‌های توسعه حرفه‌ای را در نظر بگیرید.")
        
        tips.append("\n💪 ناامید نشوید! با کمی آماده‌سازی، می‌توانید واجد شرایط بودن خود را برای برنامه‌های تحصیل در خارج بهبود دهید.")
        
        return "\n\n".join(tips)

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancel the conversation."""
        await update.message.reply_text(
            "❌ ارزیابی لغو شد. برای شروع مجدد هر زمان از /start استفاده کنید!",
            parse_mode='Markdown'
        )
        return ConversationHandler.END

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Send help message."""
        help_text = """
🤖 *راهنمای ربات بررسی واجد شرایط بودن برای تحصیل در خارج*

*دستورات:*
• /start - شروع ارزیابی واجد شرایط بودن
• /help - نمایش این پیام راهنما
• /cancel - لغو ارزیابی فعلی

*کارهای من:*
• جمع‌آوری اطلاعات تحصیلی شما
• بررسی واجد شرایط بودن شما برای تحصیل در خارج
• ارائه توصیه‌های شخصی‌سازی شده
• ارائه نکات بهبود در صورت نیاز

*معیارهای ارزیابی:*
• سن (هشدار اگر بالای ۴۰ سال)
• معدل (حداقل ۱۳ از ۲۰ توصیه می‌شود)
• مهارت زبان (حداقل سطح B1)
• پیشینه تحصیلی و اهداف

آماده شروع هستید؟ از دستور /start استفاده کنید!
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
