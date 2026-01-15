from django.contrib import admin

# Register your models here.

from .models import Category, Item, ItemRequest, City, Place

admin.site.register(Category)
admin.site.register(Item)

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'places_count')
    search_fields = ('name',)
    
    def places_count(self, obj):
        return obj.places.count()
    places_count.short_description = 'Number of Places'

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'city')
    list_filter = ('city',)
    search_fields = ('name', 'city__name')

@admin.register(ItemRequest)
class ItemRequestAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_phone', 'item', 'item_price', 'delivery_location', 'created_at', 'is_contacted')
    list_filter = ('is_contacted', 'created_at', 'item__category', 'city')
    search_fields = ('customer_name', 'customer_phone', 'item__name', 'city__name', 'place__name')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    list_editable = ('is_contacted',)
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer_name', 'customer_phone')
        }),
        ('Delivery Information', {
            'fields': ('city', 'place')
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
    
    def delivery_location(self, obj):
        if obj.city and obj.place:
            return f"{obj.city.name} - {obj.place.name}"
        elif obj.city:
            return obj.city.name
        return '-'
    delivery_location.short_description = 'Delivery Location'
    
    actions = ['mark_as_contacted', 'mark_as_not_contacted']
    
    def mark_as_contacted(self, request, queryset):
        queryset.update(is_contacted=True)
        self.message_user(request, f'{queryset.count()} requests marked as contacted.')
    mark_as_contacted.short_description = 'Mark selected as contacted'
    
    def mark_as_not_contacted(self, request, queryset):
        queryset.update(is_contacted=False)
        self.message_user(request, f'{queryset.count()} requests marked as not contacted.')
    mark_as_not_contacted.short_description = 'Mark selected as not contacted'