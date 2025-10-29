from django.shortcuts import render, redirect
from core.decorators import login_and_role_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

@login_and_role_required("customer")
def dashboard(request):
    return render(request, 'customer/dashboard.html')


@login_and_role_required("customer")
def customer_order_history(request):
    return render(request, 'customer/order-history.html')


@login_and_role_required("customer")
def customer_wish_lists(request):
    return render(request, 'customer/wish-lists.html')


@login_and_role_required("customer")
def customer_addresses(request):
    return render(request, 'customer/addresses.html')


@login_and_role_required("customer")
def customer_account_settings(request):
    return render(request, 'customer/account-settings.html')


@login_and_role_required("customer")
def password_change_view(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # logout(request)
            messages.success(request, "Password changed successfully.")
            return redirect('customer_account_settings')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
            return render(request, 'customer/account-settings.html', {'change_password_form': form})
    else:
        form = PasswordChangeForm(user=request.user)
    
        return render(request, 'customer/account-settings.html', {'change_password_form': form})
