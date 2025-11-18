from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.hashers import make_password

# Register your models here.
@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    def save_form(self, request, form, change):
            # Get the unsaved user instance
            user = super().save_form(request, form, change)

            # Hash password if it’s new or has been changed manually
            if "password" in form.cleaned_data:
                raw_password = form.cleaned_data["password"]
                # Only hash if it’s not already hashed
                if not raw_password.startswith("pbkdf2_"):
                    user.password = make_password(raw_password)
            return user