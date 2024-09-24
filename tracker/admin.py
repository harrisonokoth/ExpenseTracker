# tracker/admin.py

from django.contrib import admin
from .models import Transaction

def mark_as_completed(modeladmin, request, queryset):
    queryset.update(status='completed')

mark_as_completed.short_description = "Mark selected transactions as completed"

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('type', 'amount', 'category', 'description', 'date')
    list_filter = ('type', 'category', 'date')
    search_fields = ('description', 'category')
    actions = [mark_as_completed]

admin.site.register(Transaction, TransactionAdmin)
