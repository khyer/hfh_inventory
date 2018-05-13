from django.contrib import admin
from .models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('internal_id', 'name', 'unit_price_dollars', 'qty_in_stock', 'inventory_value', )
    search_fields = ['name']
