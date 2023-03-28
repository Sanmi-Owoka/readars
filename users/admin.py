from django.contrib import admin
from .models import User
from django.contrib.auth import admin as auth_admin


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    list_display = ["username", "email", "is_superuser"]
    search_fields = ["email", "username"]
