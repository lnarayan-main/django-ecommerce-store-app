from django.shortcuts import render, redirect
from account.forms import RegistrationForm
from django.contrib import messages
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from account.utils import send_activation_email
from account.models import User
from django.contrib.auth import authenticate, login


def home(request):
    return render(request, 'account/home.html')


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_seller:
            return redirect('seller_dashboard')
        elif request.user.is_customer:
            return redirect('customer_dashboard')
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Both fields are required.')
            return redirect('login')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect('login')
        
        if not user.is_active:
            messages.error(request, 'Your account is inactive. Please activate you account.')
            return redirect('login')
        
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)

            if user.is_seller:
                return redirect('seller_dashboard')
            elif user.is_customer:
                return redirect('customer_dashboard')
            else:
                messages.error(request, 'You do not have permission to access this area.')
                return redirect('home')
            
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')

    return render(request, 'account/login.html')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            activation_link = reverse('activate_account', kwargs={'uidb64': uidb64, 'token': token})

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

def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
        if user.is_active:
            messages.warning(request, "Your account has already been activated.")
            return redirect('login')
        
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            messages.success(request, "Your account has been activated successfully!")
            return redirect('login')
        else:
            messages.error(request, "The activation link is invalid or has expired.")
            return redirect('login')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Invalid activation link.")
        return redirect('login')
    

def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_seller:
            return redirect('seller_dashboard')
        elif request.user.is_customer:
            return redirect('customer_dashboard')
        return redirect('home')
    else:
        return redirect('home')