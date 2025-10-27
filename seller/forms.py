from django import forms
from .models import Product, ProductImage

class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'slug',
            'category',
            'description',
            'price',
            'stock',
            'sku',
            'is_active',
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
        }


# class ProductImageForm(forms.ModelForm):
#     image = forms.ImageField(
#         widget=forms.ClearableFileInput(attrs={
#         # widget=MultiFileInput(attrs={
#             # 'multiple': True,
#             'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer focus:outline-none'
#         })
#     )

#     class Meta:
#         model = ProductImage
#         fields = ['image']


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']
        widgets = {
            'image': MultiFileInput(attrs={
                'multiple': True,
                'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer focus:outline-none'
            })
        }
