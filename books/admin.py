from django.contrib import admin
from .models import Book
# Register your models here.
@admin.register(Book)
class KitAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_link = ['id', 'title']
    search_fields = ['title', 'author__username']