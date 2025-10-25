from django.shortcuts import render, redirect
from account.forms import RegistrationForm
from django.contrib import messages
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from account.utils import send_activation_email


def home(request):
    return render(request, 'account/home.html')


def login(request):
    return render(request, 'account/login.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            activation_link = reverse('', kwargs={'uidb64': uidb64, 'token': token})

            activation_url = f'{settings.SITE_DOMAIN}{activation_link}'

            send_activation_email(user.email, activation_url)

            messages.success(request, 'Registration successful! Please check your email to activate your account.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'account/register.html', {'form': form})


def password_reset(request):
    return render(request, 'account/password_reset_link.html')

def password_reset_confirm(request):
    return render(request, 'account/password_reset.html')