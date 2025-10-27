from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, 'seller/dashboard.html')


@login_required
def seller_order_history(request):
    return render(request, 'seller/order-history.html')


@login_required
def seller_wish_lists(request):
    return render(request, 'seller/wish-lists.html')


@login_required
def seller_addresses(request):
    return render(request, 'seller/addresses.html')


@login_required
def seller_account_settings(request):
    return render(request, 'seller/account-settings.html')


@login_required
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # logout(request)
            messages.success(request, "Password changed successfully.")
            return redirect('seller_account_settings')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return render(request, 'seller/account-settings.html', {'change_password_form': form})
    else:
        form = PasswordChangeForm(user=request.user)
    
        return render(request, 'seller/account-settings.html', {'change_password_form': form})