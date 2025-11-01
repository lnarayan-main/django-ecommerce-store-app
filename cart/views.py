import stripe
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from seller.models import Product
from .models import Cart, CartItem
from core.context_processors import global_context
from django.contrib import messages
import json
from core.models import Address, Order, OrderItem, Payment
from core.forms import AddressForm
from django.conf import settings
from django.db import transaction

stripe.api_key = settings.STRIPE_SECRET_KEY

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
def empty_cart(request):
    try:
        cart = Cart.objects.filter(user=request.user).first()

        if not cart:
            messages.warning(request, "Your cart is already empty.")
            return redirect('view_cart')
        
        if not cart.items.exists():
            messages.warning(request, "Your cart is already empty.")
            return redirect('view_cart')

        cart.items.all().delete()

        # no need to delete cart because may need to recreate it later again 
        # cart.delete()

        messages.success(request, "All items removed from your cart successfully!")
    except Exception as e:
        messages.error(request, f"Something went wrong while clearing the cart: {str(e)}")

    return redirect('view_cart')


@login_required
def view_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('product')
    sub_total = cart.total_price()

    taxes = 0
    shipping_charge = 0
    taxes_percentage = 0
    if sub_total:
        taxes_percentage = global_context(request)['TAX_PERCENT']
        shipping_charge = global_context(request)['SHIPPING_CHARGE']
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
    address_id = None
    address = Address.objects.filter(user=request.user, is_default=True).first()
    if address:
        address_id = address.id
        form = AddressForm(instance=address)
    else:
        form = AddressForm()

    cart = get_object_or_404(Cart, user=request.user)
    sub_total = cart.total_price()
    shipping_charge = global_context(request)['SHIPPING_CHARGE']
    taxes_percentage = global_context(request)['TAX_PERCENT']
    taxes = sub_total * taxes_percentage/100
    total = sub_total + shipping_charge + taxes

    context = {
        'address_form': form,
        'address_id': address_id,
        'sub_total' : sub_total,
        'taxes': taxes,
        'shipping_charge': shipping_charge,
        'total': total,
    }
    return render(request, 'cart/checkout.html', context)

@login_required
def payment_process(request):
    try:
        address_id = request.POST.get('address_id')
        is_different_address = request.POST.get('is_different_address')
        address = None

        if address_id == 'None':
            address_id = None

        if address_id and not is_different_address:            
            try:
                address = Address.objects.filter(id=int(address_id), user=request.user).first()
            except (ValueError, TypeError):
                address = None

            form = AddressForm(request.POST, instance=address)
            if form.is_valid():
                form.save()
        else:
            form = AddressForm(request.POST)
            if form.is_valid():
                address = form.save(commit=False)
                address.user = request.user
                address.save()

        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            messages.warning(request, "Your cart is empty.")
            return redirect('view_cart')
        sub_total = cart.total_price()
        shipping_charge = global_context(request)['SHIPPING_CHARGE']
        taxes_percentage = global_context(request)['TAX_PERCENT']
        taxes = sub_total * taxes_percentage/100

        total_amount = sub_total + shipping_charge + taxes
        total_in_cents = int(total_amount * 100)

        context = {
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'total_amount': total_amount,
            'total_in_cents': total_in_cents,
            'address': address,
        }

        return render(request, 'cart/payment.html', context)
    except Exception as e:
        print('Error! ' + str(e))
        messages.error(request, 'Error! ' + str(e))
        return redirect('checkout')


@login_required
def create_checkout_session(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    
    try:
        cart = Cart.objects.filter(user=request.user).first()
        if not cart or not cart.items.exists():
            messages.warning(request, "Your cart is empty.")
            return redirect('view_cart')

        # Get selected address
        address_id = request.POST.get('address_id')
        address = None
        if not address_id:
            messages.warning(request, 'Address not set properly.')
            return redirect('checkout')
        if address_id:
            address = Address.objects.filter(id=address_id, user=request.user).first()

        sub_total = cart.total_price()
        shipping_charge = global_context(request)['SHIPPING_CHARGE']
        taxes_percentage = global_context(request)['TAX_PERCENT']
        taxes = sub_total * taxes_percentage/100

        total_amount = sub_total + shipping_charge + taxes
        total_in_cents = int(total_amount * 100)



        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                address=address,
                total_amount=total_amount,
                sub_total= sub_total,
                tax = taxes,
                shipping_charge = shipping_charge,
            )

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.discount_price
                )

        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': f'Order #{order.id}'},
                    'unit_amount': total_in_cents,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('payment_success')) + f"?order_id={order.id}",
            cancel_url=request.build_absolute_uri(reverse('payment_cancel')) + f"?order_id={order.id}",
        )

        Payment.objects.create(
            order=order,
            user=request.user,
            amount=total_amount,
            stripe_session_id=session.id,
        )

        return JsonResponse({'success': True, 'url': session.url, 'message': 'Payment created successfully.'})

    except Address.DoesNotExist:
        return JsonResponse({'success': False,'message': 'Invalid address selected.'}, status=400)

    except Exception as e:
        print("Stripe error:", str(e))
        return JsonResponse({'success': False,'message': str(e)}, status=500)
    


def payment_success(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.filter(id=order_id, user=request.user).first()

    if order:
        payment = Payment.objects.filter(order=order).first()
        session = stripe.checkout.Session.retrieve(payment.stripe_session_id)
        payment_intent_id = session.payment_intent 
        if payment:
            payment.stripe_payment_intent = payment_intent_id
            payment.status = 'completed'
            payment.save()

        order.payment_status = 'paid'
        order.save()

        cart = Cart.objects.filter(user=request.user).first()
        cart.items.all().delete()

        messages.success(request, "Payment successful! Your order has been placed.")
    else:
        messages.warning(request, "Order not found or invalid.")

    return render(request, 'cart/payment_success.html', {'order': order})


def payment_cancel(request):
    order_id = request.GET.get('order_id')
    order = Order.objects.filter(id=order_id, user=request.user).first()

    if order:
        order.payment_status = 'cancelled'
        order.save()
        Payment.objects.filter(order=order).update(status='failed')

    messages.error(request, "Payment cancelled.")
    return render(request, 'cart/payment_cancel.html', {'order': order})


@login_required
def order_history(request):
    if request.user.is_authenticated:
        if request.user.is_seller:
            return redirect('seller_order_history')
        elif request.user.is_customer:
            return redirect('customer_order_history')
        return redirect('home')
    else:
        return redirect('home')