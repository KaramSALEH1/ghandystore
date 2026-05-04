import re

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


def validate_optional_hex(value: str) -> None:
    if not value:
        return
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", value):
        raise ValidationError("Enter a valid hex color like #RRGGBB.")

ALLOWED_SIZES = ("S", "M", "L", "XL", "XXL")


def validate_sizes(value) -> None:
    """
    Optional list of sizes. Stored as JSON for simplicity.
    Accepts: None, [] or ["S", "M", ...] (subset of ALLOWED_SIZES).
    """
    if value in (None, ""):
        return
    if not isinstance(value, list):
        raise ValidationError("Sizes must be a list.")
    for size in value:
        if size not in ALLOWED_SIZES:
            raise ValidationError(f"Invalid size '{size}'. Allowed: {', '.join(ALLOWED_SIZES)}.")


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
    sizes = models.JSONField(
        blank=True,
        null=True,
        validators=[validate_sizes],
        help_text="Optional list of sizes, e.g. [\"S\", \"M\", \"L\"]. Leave empty for no sizes.",
    )
    accent_hex = models.CharField(
        max_length=7,
        blank=True,
        default="",
        validators=[validate_optional_hex],
        help_text="Optional product accent color, e.g. #C79D4C",
    )
    image = models.ImageField(upload_to='item_images', blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='items', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def image_url(self):
        if not self.image or not self.image.name:
            return ''
        try:
            return self.image.url
        except Exception:
            return ''

    @property
    def is_out_of_stock(self):
        return bool(self.is_sold)

    @property
    def available_sizes(self):
        return self.sizes or []

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
    hex_code = models.CharField(
        max_length=7,
        blank=True,
        default="",
        validators=[validate_optional_hex],
        help_text="Optional display swatch, e.g. #4B0082",
    )
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
