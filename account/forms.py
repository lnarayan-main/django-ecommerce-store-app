from django import forms
from account.models import User


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'name', 'password', 'confirm_password', 'is_seller']

        def clean(self):
            cleaned_data = super().clean()
            password = cleaned_data.get("password")
            confirm_password = cleaned_data.get("confirm_password")

            if password != confirm_password:
                self.add_error("confirm_password", 'Password and Confirm Password do not match.')

            return cleaned_data
        
        def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("A user with this email is already exists.")
            
            return email
        

class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder':'you@example.com'})
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(('No account is associated with this email address.'))
        
        return email
    

class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_pic']

    def clean_profile_pic(self):
        image = self.cleaned_data.get('profile_pic')
        if image:
            valid_types = ['image/jpeg', 'image/png', 'image/jpg']
            max_size = 2 * 1024 * 1024  # 2MB
            if image.size > max_size:
                raise forms.ValidationError("Image size must be under 2MB.")
            if image.content_type not in valid_types:
                raise forms.ValidationError("Only JPG and PNG formats are allowed.")
        return image