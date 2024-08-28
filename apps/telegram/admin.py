from django.contrib import admin

from .models import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'telegram_id', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['first_name', 'telegram_id']
