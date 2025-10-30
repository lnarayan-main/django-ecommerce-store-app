from django import forms
from core.models import Address

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'full_name', 
            'phone_number',
            'address_line_1',
            'address_line_2',
            'city',
            'state',
            'country',
            'zip_code',
            'address_type',
            'is_default',
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-primary focus:outline-none',
                'placeholder': 'Full Name'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-primary focus:outline-none',
                'placeholder': 'Phone Number'
            }),
            'address_line_1': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-primary focus:outline-none',
                'placeholder': 'Address Line 1'
            }),
            'address_line_2': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-primary focus:outline-none',
                'placeholder': 'Address Line 2 (Optional)'
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-primary focus:outline-none',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-primary focus:outline-none',
                'placeholder': 'State'
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-primary focus:outline-none',
                'placeholder': 'Country'
            }),
            'zip_code': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-primary focus:outline-none',
                'placeholder': 'ZIP / Postal Code'
            }),
            'address_type': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:ring-2 focus:ring-primary focus:outline-none',
            }),
            'is_default': forms.CheckboxInput(attrs={
                'class': 'rounded text-primary focus:ring-primary'
            }),
        }
