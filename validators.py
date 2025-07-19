from config import LANGUAGE_LEVELS, MAJORS, DEGREE_TYPES

class Validators:
    @staticmethod
    def validate_age(age_input: str) -> bool:
        """Validate age input."""
        try:
            age = int(age_input)
            return 16 <= age <= 80
        except ValueError:
            return False

    @staticmethod
    def validate_gpa(gpa_input: str) -> bool:
        """Validate GPA input."""
        try:
            gpa = float(gpa_input)
            return 0 <= gpa <= 20
        except ValueError:
            return False

    @staticmethod
    def validate_language_level(level: str) -> bool:
        """Validate language proficiency level."""
        return level.upper() in LANGUAGE_LEVELS

    @staticmethod
    def validate_major(major: str) -> bool:
        """Validate major input."""
        return any(major.lower() in valid_major.lower() for valid_major in MAJORS) or major.lower() in ['other', 'سایر']

    @staticmethod
    def validate_degree(degree: str) -> bool:
        """Validate degree input."""
        return any(degree.lower() in valid_degree.lower() for valid_degree in DEGREE_TYPES)
