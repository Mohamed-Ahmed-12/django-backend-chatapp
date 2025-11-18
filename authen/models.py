from django.db import models
from django.contrib.auth.models import AbstractUser

# MEMBER_NAME = DB_VALUE, HUMAN_READABLE_LABEL.
class PrimaryLanguage(models.TextChoices):
    """
    Enum for Supported languages in chat 
    """
    English = 'en', 'English'
    Arabic = 'ar', 'Arabic'
    
# Operation,Code Example,Output/Result
# Set a Value,     user.primary_lng = PrimaryLanguage.Arabic,      Sets the field's value to the string 'ar'.
# Check a Value    user.primary_lng == PrimaryLanguage.English:,   Checks if the stored string is 'en'.
# Get DB Value,    PrimaryLanguage.Arabic.value,                   Returns the string 'ar'.
# Get Label,       PrimaryLanguage.Arabic.label,                   Returns the string 'Arabic'.
# Get Display,     user.get_primary_lng_display(),                 Returns the human-readable string 'English' (or 'Arabic') by using Django's built-in helper method.

class CustomUser(AbstractUser):
    primary_lng = models.CharField(verbose_name="Primary Language" , max_length=3 , choices=PrimaryLanguage.choices ,default=PrimaryLanguage.English )
