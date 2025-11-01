from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'phone', 'created_at', 'updated_at']
    search_fields = ['name', 'email', 'phone']
    list_filter = ['created_at', 'updated_at']
    readonly_fields = ['created_at', 'updated_at']

