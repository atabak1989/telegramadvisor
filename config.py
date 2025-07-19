import os

# Bot configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'your_bot_token_here')

# Conversation states
AGE, MAJOR, DEGREE, BACHELOR_FIELD, MASTER_FIELD, GPA, LANGUAGE, BUDGET, COUNTRY = range(9)

# Language proficiency levels (ordered from lowest to highest)
LANGUAGE_LEVELS = {
    'A1': 1,
    'A2': 2,
    'B1': 3,
    'B2': 4,
    'C1': 5,
    'C2': 6
}

# Minimum requirements
MIN_GPA = 13.0
MAX_AGE = 40
MIN_LANGUAGE_LEVEL = 'B1'

# Available degree types
DEGREE_TYPES = [
    'مدرک کارشناسی',
    'مدرک کارشناسی ارشد',
    'دکتری',
    'مدرک فوق دیپلم',
    'دیپلم',
    'دیپلم دبیرستان'
]

# Available majors
MAJORS = [
    'علوم کامپیوتر',
    'مهندسی',
    'مدیریت بازرگانی',
    'پزشکی',
    'حقوق',
    'هنر',
    'علوم',
    'آموزش و پرورش',
    'اقتصاد',
    'روانشناسی',
    'سایر'
]

# Budget ranges
BUDGET_RANGES = [
    'کمتر از ۲ میلیارد تومان',
    'بین ۲ تا ۳ میلیارد تومان', 
    'بیشتر از ۳ میلیارد تومان'
]

# Country recommendations based on budget
BUDGET_COUNTRIES = {
    'low': ['ایتالیا', 'آلمان', 'اتریش', 'ترکیه', 'روسیه'],
    'medium': ['ایتالیا', 'آلمان', 'اتریش', 'ترکیه', 'روسیه', 'هلند', 'سوئد', 'دانمارک', 'فنلاند'],
    'high': ['ایتالیا', 'آلمان', 'اتریش', 'ترکیه', 'روسیه', 'هلند', 'سوئد', 'دانمارک', 'فنلاند', 'کانادا', 'انگلستان', 'استرالیا']
}
