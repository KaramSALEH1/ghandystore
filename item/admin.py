from django.contrib import admin
from django.utils.html import format_html

# Register your models here.

from .models import Category, Item, ItemRequest, City, Place, ItemColor, ItemColorImage

admin.site.register(Category)

class ItemColorImageInline(admin.TabularInline):
    model = ItemColorImage
    extra = 3
    fields = ('image',)
    verbose_name = 'Color Image'
    verbose_name_plural = 'Color Images'

class ItemColorInline(admin.StackedInline):
    model = ItemColor
    extra = 1
    fields = ('name', 'is_sold_out', 'images_info', 'edit_link')
    readonly_fields = ('images_info', 'edit_link')
    
    def images_info(self, obj):
        if obj.pk:
            images = obj.images.all()
            if images:
                html = '<div style="margin: 10px 0;"><strong>Images ({})</strong><div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px;">'.format(images.count())
                for img in images:
                    html += f'<img src="{img.image.url}" style="max-height: 80px; max-width: 80px; border: 1px solid #ddd; padding: 5px; border-radius: 4px;" />'
                html += '</div></div>'
                return format_html(html)
            return format_html('<p style="color: #999; font-style: italic; margin: 10px 0;">No images yet. Click "Edit Color" below to add images.</p>')
        return format_html('<p style="color: #999; font-style: italic; margin: 10px 0;">💡 Save this item first, then click "Edit Color" to add images.</p>')
    images_info.short_description = 'Images'
    
    def edit_link(self, obj):
        if obj.pk:
            url = f'/admin/item/itemcolor/{obj.pk}/change/'
            return format_html('<a href="{}" target="_blank" style="display: inline-block; margin-top: 10px; padding: 8px 16px; background: #417690; color: white; text-decoration: none; border-radius: 4px; font-size: 13px;">📷 Edit Color & Add Images</a>', url)
        return format_html('<p style="color: #999; font-size: 12px; margin-top: 10px;">Save item first to add images</p>')
    edit_link.short_description = 'Actions'

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_sold', 'created_by', 'created_at')
    list_filter = ('category', 'is_sold', 'created_at')
    search_fields = ('name', 'description')
    inlines = [ItemColorInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('category', 'name', 'description', 'price', 'image')
        }),
        ('Status', {
            'fields': ('is_sold',)
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at',)
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(ItemColor)
class ItemColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'item', 'is_sold_out', 'images_count', 'created_at')
    list_filter = ('is_sold_out', 'created_at', 'item__category')
    search_fields = ('name', 'item__name')
    readonly_fields = ('created_at',)
    inlines = [ItemColorImageInline]
    
    def images_count(self, obj):
        return obj.images.count()
    images_count.short_description = 'Images'

@admin.register(ItemColorImage)
class ItemColorImageAdmin(admin.ModelAdmin):
    list_display = ('color', 'image_preview', 'created_at')
    list_filter = ('created_at', 'color__item__category')
    search_fields = ('color__name', 'color__item__name')
    readonly_fields = ('created_at', 'image_preview')
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 100px; max-width: 100px;" />', obj.image.url)
        return 'No image'
    image_preview.short_description = 'Preview'

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
    list_display = ('customer_name', 'customer_phone', 'item', 'color', 'item_price', 'delivery_location', 'created_at', 'is_contacted')
    list_filter = ('is_contacted', 'created_at', 'item__category', 'city', 'color')
    search_fields = ('customer_name', 'customer_phone', 'item__name', 'color__name', 'city__name', 'place__name')
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
            'fields': ('item', 'color')
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