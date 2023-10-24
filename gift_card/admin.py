from django.contrib import admin
from .models import Card


class CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'number', 'nominal', 'created', 'modified')
    search_fields = ['user__username', 'card_number']  # Добавьте поля для поиска

admin.site.register(Card, CardAdmin)
