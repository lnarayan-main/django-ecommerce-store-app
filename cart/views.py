from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from seller.models import Product
from .models import Cart, CartItem
from core.context_processors import global_context
from django.contrib import messages
import json

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart, created = Cart.objects.get_or_create(user=request.user)
    item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not item_created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    return JsonResponse({'success': True, 'cart_count': cart.items.count(), 'message': 'Item added to cart!'})


@login_required
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('view_cart')
    # return JsonResponse({'success': True, 'message': 'Item removed from cart.'})


@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product')
    sub_total = cart.total_price()

    taxes = 0
    shipping_charge = 0
    taxes_percentage = global_context(request)['TAX_PERCENT']
    shipping_charge = global_context(request)['SHIPPING_CHARGE']
    if sub_total:
        taxes = (sub_total * taxes_percentage) / 100 
    total = sub_total + taxes + shipping_charge

    context = {
        'cart': cart, 
        'items': items, 
        'sub_total': sub_total, 
        'taxes': taxes, 
        'shipping_charge': shipping_charge, 
        'total': total,
        'tax_percent': taxes_percentage
    }

    return render(request, 'cart/cart-items.html', context)


@login_required
def update_cart(request):
    if request.method == 'POST':
        form_data = request.POST.get('cart_data')
        cart_data = json.loads(form_data)

        cart, _ = Cart.objects.get_or_create(user=request.user)

        for item in cart_data:
            product = get_object_or_404(Product, id=item.get('product_id'))
            quantity = int(item.get('quantity'))

            item, _ = CartItem.objects.get_or_create(cart=cart, product=product)

            item.quantity = quantity
            item.save()
        return JsonResponse({'success': True, 'message': 'Cart updated successfully'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
    
@login_required
def checkout(request):
    return render(request, 'cart/checkout.html')
