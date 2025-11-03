from django import forms
from .models import Product, ProductImage

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultiFileInput(
             attrs={
                "class": (
                    "block w-full text-sm text-gray-900 border border-gray-300 "
                    "rounded-lg cursor-pointer bg-gray-50 focus:outline-none"
                ),
                "multiple": True,
                "accept": "image/*",
                "onchange":"previewImages(event)",
            }
        ))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'slug',
            'category',
            'brand',
            'description',
            'price',
            'discount_price',
            'stock',
            'sku',
            'is_active',
            'available_sizes',     
            'available_colors', 
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border rounded-md p-2 focus:ring-2 focus:ring-primary focus:outline-none',
                'placeholder': 'Enter product name'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full border rounded-md p-2 focus:ring-2 focus:ring-primary focus:outline-none',
                'placeholder': 'Auto-generated or custom slug'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full border rounded-md p-2 focus:ring-2 focus:ring-primary focus:outline-none',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border rounded-md p-2 focus:ring-2 focus:ring-primary focus:outline-none',
                'rows': 4,
                'placeholder': 'Write a short description about the product...'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'w-full border rounded-md p-2 focus:ring-2 focus:ring-primary focus:outline-none',
                'min': '0'
            }),
            'discount_price': forms.NumberInput(attrs={
                'class': 'w-full border rounded-md p-2 focus:ring-2 focus:ring-primary focus:outline-none',
                'min': '0'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'w-full border rounded-md p-2 focus:ring-2 focus:ring-primary focus:outline-none',
                'min': '0'
            }),
            'sku': forms.TextInput(attrs={
                'class': 'w-full border rounded-md p-2 focus:ring-2 focus:ring-primary focus:outline-none',
                'placeholder': 'e.g., SKU12345'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-5 w-5 text-primary focus:ring-primary'
            }),

            'brand': forms.Select(attrs={
                'class': 'w-full border rounded-md p-2 focus:ring-2 focus:ring-primary focus:outline-none',
            }),

            'available_sizes': forms.SelectMultiple(attrs={
                'class': 'w-full border rounded-md p-2 focus:ring-2 focus:ring-primary focus:outline-none h-32', 
                'size': '5', # Shows 5 options at once
            }),
            'available_colors': forms.SelectMultiple(attrs={
                # Adjusted size for better visibility of multiple selections
                'class': 'w-full border rounded-md p-2 focus:ring-2 focus:ring-primary focus:outline-none h-32',
                'size': '3', # Shows 3 options at once
            }),
        }




class ProductImageForm(forms.Form):
    image = MultipleFileField()

    def __init__(self, *args, **kwargs):
        require_images = kwargs.pop('require_images', False)
        super().__init__(*args, **kwargs)
        self.fields['image'].required = require_images

    class Meta:
        model = ProductImage
        fields = ['image']