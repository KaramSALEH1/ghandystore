from django.contrib import admin

# Register your models here.

from .models import Category, Item, ItemRequest

admin.site.register(Category)
admin.site.register(Item)

@admin.register(ItemRequest)
class ItemRequestAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_phone', 'item', 'item_price', 'created_at', 'is_contacted', 'has_message')
    list_filter = ('is_contacted', 'created_at', 'item__category')
    search_fields = ('customer_name', 'customer_phone', 'item__name', 'message')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    list_editable = ('is_contacted',)
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_phone', 'message')
        }),
        ('Item Information', {
            'fields': ('item',)
        }),
        ('Status', {
            'fields': ('is_contacted', 'created_at')
        }),
    )
    
    def item_price(self, obj):
        return f"{obj.item.price} SYP"
    item_price.short_description = 'Item Price'
    
    def has_message(self, obj):
        return '✓' if obj.message else '✗'
    has_message.short_description = 'Message'
    
    actions = ['mark_as_contacted', 'mark_as_not_contacted']
    
    def mark_as_contacted(self, request, queryset):
        queryset.update(is_contacted=True)
        self.message_user(request, f'{queryset.count()} requests marked as contacted.')
    mark_as_contacted.short_description = 'Mark selected as contacted'
    
    def mark_as_not_contacted(self, request, queryset):
        queryset.update(is_contacted=False)
        self.message_user(request, f'{queryset.count()} requests marked as not contacted.')
    mark_as_not_contacted.short_description = 'Mark selected as not contacted'