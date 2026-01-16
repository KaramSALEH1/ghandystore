from django import forms

from .models import Item, ItemRequest, City, Place, ItemColor

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('category', 'name', 'description', 'price', 'image',)
        widgets = {
            'category': forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }

class EditItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'price', 'image', 'is_sold')
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            }),
            'price': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }

class ItemRequestForm(forms.ModelForm):
    class Meta:
        model = ItemRequest
        fields = ('color', 'customer_name', 'customer_phone', 'city', 'place')
        widgets = {
            'color': forms.Select(attrs={
                'class': INPUT_CLASSES,
                'id': 'id_color'
            }),
            'customer_name': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'الاسم الثلاثي الكامل'
            }),
            'customer_phone': forms.TextInput(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'رقم الهاتف للتواصل',
                'type': 'tel'
            }),
            'city': forms.Select(attrs={
                'class': INPUT_CLASSES,
                'id': 'id_city'
            }),
            'place': forms.Select(attrs={
                'class': INPUT_CLASSES,
                'placeholder': 'شركة الشحن هي مسارات و القدموس فقط في حال عدم تواجد فرع مسارات',
                'id': 'id_place',
            })
        }
        labels = {
            'color': 'Color',
            'customer_name': 'Name',
            'customer_phone': 'Phone Number',
            'city': 'City',
            'place': 'Place of Delivery'
        }
    
    def __init__(self, *args, **kwargs):
        self.item = kwargs.pop('item', None)
        super().__init__(*args, **kwargs)
        
        # Set color queryset based on item
        if self.item:
            self.fields['color'].queryset = ItemColor.objects.filter(
                item=self.item, 
                is_sold_out=False
            ).order_by('name')
            if self.fields['color'].queryset.exists():
                self.fields['color'].required = True
            else:
                self.fields['color'].required = False
                self.fields['color'].widget.attrs['style'] = 'display:none;'
        else:
            self.fields['color'].queryset = ItemColor.objects.none()
            self.fields['color'].required = False
        
        self.fields['city'].required = True
        self.fields['place'].required = True
        self.fields['city'].queryset = City.objects.all().order_by('name')
        self.fields['place'].queryset = Place.objects.none()
        
        if 'city' in self.data:
            try:
                city_id = int(self.data.get('city'))
                self.fields['place'].queryset = Place.objects.filter(city_id=city_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            if self.instance.city:
                self.fields['place'].queryset = self.instance.city.places.order_by('name')
    
    def clean(self):
        cleaned_data = super().clean()
        city = cleaned_data.get('city')
        place = cleaned_data.get('place')
        color = cleaned_data.get('color')
        
        if city and place:
            if place.city != city:
                raise forms.ValidationError({
                    'place': 'Selected place does not belong to the selected city.'
                })
        
        if color and self.item:
            if color.item != self.item:
                raise forms.ValidationError({
                    'color': 'Selected color does not belong to this item.'
                })
            if color.is_sold_out:
                raise forms.ValidationError({
                    'color': 'This color is sold out.'
                })
        
        return cleaned_data