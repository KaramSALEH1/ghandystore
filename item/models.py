from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Item(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField()
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Cities'
    
    def __str__(self):
        return self.name

class Place(models.Model):
    city = models.ForeignKey(City, related_name='places', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Places'
    
    def __str__(self):
        return f"{self.city.name} - {self.name}"

class ItemColor(models.Model):
    item = models.ForeignKey(Item, related_name='colors', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    is_sold_out = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('name',)
        unique_together = ('item', 'name')  # Prevent duplicate colors for same item
    
    def __str__(self):
        return f"{self.item.name} - {self.name}"

class ItemColorImage(models.Model):
    color = models.ForeignKey(ItemColor, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='item_color_images')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('created_at',)
    
    def __str__(self):
        return f"{self.color.item.name} - {self.color.name} - Image"

class ItemRequest(models.Model):
    item = models.ForeignKey(Item, related_name='requests', on_delete=models.CASCADE)
    color = models.ForeignKey(ItemColor, related_name='requests', on_delete=models.SET_NULL, null=True, blank=True)
    customer_name = models.CharField(max_length=255)
    customer_phone = models.CharField(max_length=20)
    city = models.ForeignKey(City, related_name='requests', on_delete=models.SET_NULL, null=True, blank=True)
    place = models.ForeignKey(Place, related_name='requests', on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_contacted = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        color_info = f" - {self.color.name}" if self.color else ""
        return f"{self.customer_name} - {self.item.name}{color_info}"