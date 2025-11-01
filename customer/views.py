from django.shortcuts import render, redirect, get_object_or_404
from core.decorators import login_and_role_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from core.models import Order, Address
from core.forms import AddressForm

@login_and_role_required("customer")
def dashboard(request):
    return render(request, 'customer/dashboard.html')


@login_and_role_required("customer")
def customer_order_history(request):
    orders = Order.objects.filter(user=request.user).prefetch_related('items__product', 'payment')
    return render(request, 'customer/order-history.html', {'orders': orders})


@login_and_role_required("customer")
def customer_wish_lists(request):
    return render(request, 'customer/wish-lists.html')



@login_and_role_required("customer")
def customer_account_settings(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        user = request.user
        
        if name:
            user.name = name
        if email:
            user.email = email
            
        user.save()
        
        messages.success(request, 'Details updated successfully.') 
        
        return redirect('seller_account_settings')
        
    else:
        context = {
            'user': request.user
        }
    return render(request, 'customer/account-settings.html', context)


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
    

@login_and_role_required('customer')
def order_details(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related('address', 'payment').prefetch_related('items__product'),
        id=order_id,
        user=request.user
    )
    context = {'order': order}
    return render(request, 'customer/order-details.html', context)


@login_and_role_required("customer")
def customer_addresses(request, address_id=None):
    default_address = Address.objects.filter(user=request.user, is_default=True).first()
    addresses = Address.objects.filter(user=request.user, is_default=False).order_by('-created_at')
    if request.method == 'POST':
        if address_id is not None:
            address = get_object_or_404(Address, id=address_id, user=request.user)
            form = AddressForm(request.POST, instance=address)
        else:
            form = AddressForm(request.POST)

        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            messages.success(request, 'Address saved successfully!')
            return redirect('customer_addresses')
    else:
        if address_id is not None:
            address = get_object_or_404(Address, id=address_id, user=request.user)
            form = AddressForm(instance=address)
        else:
            form = AddressForm()

    context = {
        'form': form,
        'default_address': default_address,
        'addresses': addresses,
        'address_id':address_id,
    }

    return render(request, 'customer/addresses.html', context)


@login_and_role_required('customer')
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    if address:
        address.delete()
    messages.success(request, 'Address deleted successfully.')
    return redirect('customer_addresses')