import json
import random
from typing import Dict, List

class RecommendationEngine:
    def __init__(self):
        self.study_programs = self._load_study_programs()
        self.countries_data = self._load_countries_data()

    def _load_study_programs(self):
        """Load study programs from JSON file."""
        try:
            with open('data/study_programs.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_programs()

    def _load_countries_data(self):
        """Load countries data from JSON file."""
        try:
            with open('data/countries.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._get_default_countries()

    def get_recommendations(self, user_data: Dict) -> str:
        """
        Generate personalized study abroad recommendations based on user profile.
        """
        preferred_country = user_data.get('preferred_country', '').lower()
        major = user_data.get('major', '')
        degree = user_data.get('degree', '')
        gpa = user_data.get('gpa', 0)
        language_level = user_data.get('language_level', 'B1')
        
        recommendations = ["🎯 *توصیه‌های شخصی‌سازی شده برای تحصیل در خارج*\n"]
        
        # Find matching country
        country_info = self._find_country_info(preferred_country)
        if country_info:
            recommendations.append(f"🌍 *مقصد توصیه شده: {country_info['name']}*")
            recommendations.append(f"• {country_info['description']}")
            recommendations.append(f"• نیازمندی زبان: {country_info['language_requirement']}")
            recommendations.append(f"• متوسط شهریه: {country_info['avg_tuition']}")
            recommendations.append(f"• مهلت ثبت نام: {country_info['application_deadline']}")
        
        # Find matching programs
        matching_programs = self._find_matching_programs(major, degree, gpa)
        if matching_programs:
            recommendations.append(f"\n📚 *برنامه‌های توصیه شده:*")
            for i, program in enumerate(matching_programs[:3], 1):
                recommendations.append(f"\n*{i}. {program['name']}*")
                recommendations.append(f"• مدت زمان: {program['duration']}")
                recommendations.append(f"• نیازمندی‌ها: {program['requirements']}")
                recommendations.append(f"• زمینه‌های تمرکز: {', '.join(program['focus_areas'])}")
        
        # Add scholarship information
        recommendations.append(f"\n💰 *فرصت‌های بورسیه:*")
        scholarships = self._get_relevant_scholarships(gpa, major, country_info)
        for scholarship in scholarships:
            recommendations.append(f"• {scholarship}")
        
        # Add next steps
        recommendations.append(f"\n📋 *مراحل بعدی:*")
        next_steps = self._get_next_steps(user_data, country_info)
        for step in next_steps:
            recommendations.append(f"• {step}")
        
        # Add timeline
        recommendations.append(f"\n⏰ *زمان‌بندی توصیه شده:*")
        timeline = self._get_application_timeline()
        for item in timeline:
            recommendations.append(f"• {item}")
        
        return "\n".join(recommendations)

    def _find_country_info(self, preferred_country: str):
        """Find information about the preferred country."""
        for country in self.countries_data.get('countries', []):
            if preferred_country in country['name'].lower() or any(alias.lower() in preferred_country for alias in country.get('aliases', [])):
                return country
        return None

    def _find_matching_programs(self, major: str, degree: str, gpa: float):
        """Find study programs matching user's profile."""
        matching_programs = []
        
        for program in self.study_programs.get('programs', []):
            # Check if major matches
            if major.lower() in [field.lower() for field in program.get('fields', [])]:
                # Check GPA requirement
                min_gpa = program.get('min_gpa', 0)
                if gpa >= min_gpa:
                    # Check degree level compatibility
                    if self._is_degree_compatible(degree, program.get('level', '')):
                        matching_programs.append(program)
        
        # Sort by relevance (higher GPA requirements first, then by name)
        matching_programs.sort(key=lambda x: (-x.get('min_gpa', 0), x.get('name', '')))
        
        return matching_programs

    def _is_degree_compatible(self, user_degree: str, program_level: str):
        """Check if user's degree is compatible with program level."""
        degree_hierarchy = {
            'high school diploma': 1,
            'associate degree': 2,
            'bachelor\'s degree': 3,
            'master\'s degree': 4,
            'phd/doctorate': 5
        }
        
        user_level = degree_hierarchy.get(user_degree.lower(), 0)
        
        # For undergraduate programs, need high school or associate
        if 'undergraduate' in program_level.lower() or 'bachelor' in program_level.lower():
            return user_level <= 2
        
        # For graduate programs, need bachelor's or higher
        if 'graduate' in program_level.lower() or 'master' in program_level.lower():
            return user_level >= 3
        
        # For PhD programs, need master's or higher
        if 'phd' in program_level.lower() or 'doctorate' in program_level.lower():
            return user_level >= 4
        
        return True

    def _get_relevant_scholarships(self, gpa: float, major: str, country_info):
        """Get relevant scholarship opportunities."""
        scholarships = []
        
        if gpa >= 18:
            scholarships.append("بورسیه تعالی (پوشش کامل شهریه)")
        elif gpa >= 16:
            scholarships.append("بورسیه شایستگی (پوشش ۵۰-۷۵٪ شهریه)")
        elif gpa >= 14:
            scholarships.append("جایزه موفقیت تحصیلی (پوشش ۲۵-۵۰٪ شهریه)")
        
        if country_info:
            country_name = country_info.get('name', '')
            scholarships.append(f"برنامه بورسیه دولتی {country_name}")
            scholarships.append(f"صندوق حمایت از دانشجویان بین‌المللی - {country_name}")
        
        if major.lower() in ['علوم کامپیوتر', 'مهندسی', 'علوم']:
            scholarships.append("کمک هزینه تعالی STEM")
        
        if not scholarships:
            scholarships.append("کمک مالی بر اساس نیاز")
            scholarships.append("صندوق اضطراری دانشجویان بین‌المللی")
        
        return scholarships

    def _get_next_steps(self, user_data: Dict, country_info):
        """Generate personalized next steps."""
        steps = []
        
        # Language preparation
        language_level = user_data.get('language_level', 'B1')
        if language_level in ['B1', 'B2']:
            steps.append("بهبود مهارت زبان به سطح C1 برای فرصت‌های بیشتر را در نظر بگیرید")
        
        # Documentation
        steps.append("ریز نمرات رسمی و گواهی‌های مدرک تحصیلی را آماده کنید")
        steps.append("توصیه‌نامه‌هایی از اساتید/کارفرمایان جمع‌آوری کنید")
        
        # Country-specific requirements
        if country_info:
            steps.append(f"نیازمندی‌های ویزا برای {country_info['name']} را بررسی کنید")
            if 'additional_requirements' in country_info:
                for req in country_info['additional_requirements']:
                    steps.append(req)
        
        # Application process
        steps.append("بیانیه شخصی/نامه انگیزه جذابی بنویسید")
        steps.append("دانشگاه‌های مناسب را تحقیق کرده و با آن‌ها تماس بگیرید")
        steps.append("برای آزمون‌های استاندارد در صورت نیاز آماده شوید (IELTS, TOEFL, GRE و غیره)")
        
        return steps

    def _get_application_timeline(self):
        """Get recommended application timeline."""
        return [
            "۱۲ ماه قبل: شروع آماده‌سازی زبان و تحقیق",
            "۹ ماه قبل: شرکت در آزمون‌های استاندارد، جمع‌آوری مدارک",
            "۶ ماه قبل: ارسال درخواست‌ها و درخواست بورسیه",
            "۳ ماه قبل: آماده‌سازی درخواست ویزا و اقامت",
            "۱ ماه قبل: آماده‌سازی نهایی و ترتیبات سفر"
        ]

    def _get_default_programs(self):
        """Return default study programs if file is not available."""
        return {
            "programs": [
                {
                    "name": "International Business Administration",
                    "fields": ["Business Administration", "Economics"],
                    "level": "Graduate",
                    "duration": "2 years",
                    "min_gpa": 14.0,
                    "requirements": "Bachelor's degree, IELTS 6.5+",
                    "focus_areas": ["Global Management", "International Trade", "Strategic Planning"]
                },
                {
                    "name": "Computer Science & Engineering",
                    "fields": ["Computer Science", "Engineering"],
                    "level": "Graduate",
                    "duration": "2 years",
                    "min_gpa": 15.0,
                    "requirements": "Bachelor's in related field, IELTS 6.5+",
                    "focus_areas": ["AI/ML", "Software Engineering", "Data Science"]
                },
                {
                    "name": "International Relations",
                    "fields": ["Law", "Arts", "Sciences"],
                    "level": "Graduate", 
                    "duration": "2 years",
                    "min_gpa": 13.5,
                    "requirements": "Bachelor's degree, IELTS 6.0+",
                    "focus_areas": ["Diplomacy", "Global Politics", "International Law"]
                }
            ]
        }

    def _get_default_countries(self):
        """Return default countries data if file is not available."""
        return {
            "countries": [
                {
                    "name": "United States",
                    "aliases": ["USA", "US", "America"],
                    "description": "World-renowned universities with diverse programs and research opportunities",
                    "language_requirement": "TOEFL 80+ or IELTS 6.5+",
                    "avg_tuition": "$20,000-60,000 per year",
                    "application_deadline": "December-February",
                    "additional_requirements": ["SAT/GRE scores may be required", "Financial statement required"]
                },
                {
                    "name": "Canada",
                    "aliases": ["CA"],
                    "description": "High-quality education with post-graduation work opportunities",
                    "language_requirement": "IELTS 6.5+ or TOEFL 90+",
                    "avg_tuition": "$15,000-35,000 CAD per year",
                    "application_deadline": "January-March",
                    "additional_requirements": ["Study permit required", "Medical exam may be required"]
                },
                {
                    "name": "United Kingdom",
                    "aliases": ["UK", "Britain", "England"],
                    "description": "Prestigious universities with rich academic tradition",
                    "language_requirement": "IELTS 6.5+ or TOEFL 90+",
                    "avg_tuition": "£15,000-45,000 per year",
                    "application_deadline": "January (UCAS deadline)",
                    "additional_requirements": ["UCAS application required", "Tier 4 student visa"]
                }
            ]
        }
