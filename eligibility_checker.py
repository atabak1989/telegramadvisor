from config import MIN_GPA, MAX_AGE, MIN_LANGUAGE_LEVEL, LANGUAGE_LEVELS

class EligibilityChecker:
    def __init__(self):
        self.min_gpa = MIN_GPA
        self.max_age = MAX_AGE
        self.min_language_level = MIN_LANGUAGE_LEVEL

    def assess_eligibility(self, user_data):
        """
        Assess user eligibility based on collected data.
        Returns a dictionary with eligibility status and detailed message.
        """
        issues = []
        warnings = []
        
        # Check age
        age = user_data.get('age', 0)
        if age > self.max_age:
            warnings.append(f"سن بالای {self.max_age} سال (فعلی: {age})")
        
        # Check GPA
        gpa = user_data.get('gpa', 0)
        if gpa < self.min_gpa:
            issues.append(f"معدل کمتر از {self.min_gpa} از ۲۰ (فعلی: {gpa} از ۲۰)")
        
        # Check language proficiency
        language_level = user_data.get('language_level', 'A1')
        min_level_value = LANGUAGE_LEVELS.get(self.min_language_level, 3)
        current_level_value = LANGUAGE_LEVELS.get(language_level, 1)
        
        if current_level_value < min_level_value:
            issues.append(f"سطح زبان کمتر از {self.min_language_level} (فعلی: {language_level})")
        
        # Determine eligibility
        eligible = len(issues) == 0
        
        # Create response message
        message = self._create_assessment_message(user_data, eligible, issues, warnings)
        
        return {
            'eligible': eligible,
            'issues': issues,
            'warnings': warnings,
            'message': message
        }

    def _create_assessment_message(self, user_data, eligible, issues, warnings):
        """Create a formatted assessment message."""
        
        # Header
        if eligible:
            message = ["🎉 *تبریک! شما واجد شرایط برنامه‌های تحصیل در خارج هستید!*\n"]
            message.append("✅ *خلاصه پروفایل شما:*")
        else:
            message = ["❌ *وضعیت فعلی واجد شرایط بودن: واجد شرایط نیستید*\n"]
            message.append("📋 *خلاصه پروفایل شما:*")
        
        # Profile summary
        message.append(f"• سن: {user_data.get('age')} سال")
        message.append(f"• رشته: {user_data.get('major')}")
        message.append(f"• مدرک: {user_data.get('degree')}")
        message.append(f"• معدل: {user_data.get('gpa')} از ۲۰")
        message.append(f"• سطح زبان: {user_data.get('language_level')}")
        message.append(f"• کشور مورد علاقه: {user_data.get('preferred_country')}")
        
        # Assessment results
        message.append("\n📊 *نتایج ارزیابی:*")
        
        # Check each criterion
        age = user_data.get('age', 0)
        if age <= self.max_age:
            message.append(f"✅ سن: عالی (≤{self.max_age})")
        else:
            message.append(f"⚠️ سن: بالاتر از محدوده ترجیحی (>{self.max_age})")
        
        gpa = user_data.get('gpa', 0)
        if gpa >= self.min_gpa:
            message.append(f"✅ معدل: واجد شرایط (≥{self.min_gpa} از ۲۰)")
        else:
            message.append(f"❌ معدل: کمتر از حداقل ({self.min_gpa} از ۲۰ مورد نیاز)")
        
        language_level = user_data.get('language_level', 'A1')
        min_level_value = LANGUAGE_LEVELS.get(self.min_language_level, 3)
        current_level_value = LANGUAGE_LEVELS.get(language_level, 1)
        
        if current_level_value >= min_level_value:
            message.append(f"✅ زبان: واجد شرایط (≥{self.min_language_level})")
        else:
            message.append(f"❌ زبان: کمتر از حداقل ({self.min_language_level} مورد نیاز)")
        
        # Issues and next steps
        if issues:
            message.append(f"\n🚫 *مسائل قابل بررسی:*")
            for issue in issues:
                message.append(f"• {issue}")
        
        if warnings:
            message.append(f"\n⚠️ *نکات:*")
            for warning in warnings:
                message.append(f"• {warning}")
        
        return "\n".join(message)
