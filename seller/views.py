from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from core.decorators import login_and_role_required
from seller.models import Product, ProductImage
from django.db.models import Q
from django.core.paginator import Paginator
from seller.forms import ProductForm, ProductImageForm
from django.db import transaction
import os

@login_and_role_required("seller")
def dashboard(request):
    return render(request, 'seller/dashboard.html')


@login_and_role_required("seller")
def seller_order_history(request):
    return render(request, 'seller/order-history.html')


@login_and_role_required("seller")
def seller_wish_lists(request):
    return render(request, 'seller/wish-lists.html')


@login_and_role_required("seller")
def seller_addresses(request):
    return render(request, 'seller/addresses.html')


@login_and_role_required("seller")
def seller_account_settings(request):
    return render(request, 'seller/account-settings.html')


@login_and_role_required("seller")
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
    

@login_and_role_required('seller')
def products_list(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(seller=request.user).all().order_by('-created_at')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(category__name__icontains=query) |
            Q(description__icontains=query)
        )

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'products': page_obj,
        'query': query
    }
    return render(request, 'seller/products-list.html', context)


@login_and_role_required('seller')
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        image_form = ProductImageForm(request.POST, request.FILES)

        try:
            if form.is_valid() and image_form.is_valid():
                with transaction.atomic():  # Ensures atomic DB operation
                    product = form.save(commit=False)
                    product.seller = request.user
                    product.save()

                    images = request.FILES.getlist('image')
                    if not images:
                        messages.warning(request, "⚠️ No images uploaded for this product.")
                    else:
                        for img in images:
                            ProductImage.objects.create(product=product, image=img)

                    messages.success(request, '✅ Product created successfully!')
                    return redirect('products_list')

            else:
                # Collect all validation errors for debugging
                form_errors = form.errors.as_json()
                image_errors = image_form.errors.as_json()
                messages.error(request, f"❌ Validation failed! {form_errors} {image_errors}")

        except Exception as e:
            # Specific error details for debugging
            messages.error(request, f"🚨 Unexpected Error: {type(e).__name__} — {e}")

    else:
        form = ProductForm()
        image_form = ProductImageForm()

    context = {
        'form': form,
        'image_form': image_form,
    }
    return render(request, 'seller/create-product.html', context)



@login_and_role_required('seller')
def product_edit(request, product_id):
    return render(request, 'seller/create-product.html')

@login_and_role_required('seller')
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    for img in product.images.all():
        if img.image and os.path.isfile(img.image.path):
            os.remove(img.image.path)
        img.delete()

    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('products_list')
