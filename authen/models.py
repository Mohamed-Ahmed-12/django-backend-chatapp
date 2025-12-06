from django.db import models
from django.contrib.auth.models import AbstractUser

# MEMBER_NAME = DB_VALUE, HUMAN_READABLE_LABEL.
class PrimaryLanguage(models.TextChoices):
    """
    Enum for Supported languages in chat 
    """
    English = 'eng_Latn', 'English'
    Arabic = 'arb_Arab', 'Arabic'
    French = 'fra_Latn', 'French'
    German = 'deu_Latn', 'German'
    Russian = 'rus_Cyrl', 'Russian'


class CustomUser(AbstractUser):
    primary_lng = models.CharField(verbose_name="Primary Language" , max_length=25 , choices=PrimaryLanguage.choices ,default=PrimaryLanguage.English )
    pic = models.ImageField(upload_to='userimgs',blank=True,null=True)
    is_searchable = models.BooleanField(default=True, help_text="enable public user",blank=True,null=True)