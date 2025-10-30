from core.models import Category
import os
from django.conf import settings
from cart.models import Cart

def categories_processor(request):
    categories = Category.objects.filter(parent=None).order_by('pk').prefetch_related('subcategories')
    return {
        'header_categories': categories
    }

def global_context(request):
    """
    Adds global variables like APP_NAME to the template context 
    automatically for every request.
    """
    app_name = getattr(settings, 'APP_NAME', 'Django App')
    shipping_charge = getattr(settings, 'SHIPPING_CHARGE', 5)
    tax_percent = getattr(settings, 'TAX_PERCENT', 5)
    
    return {
        'APP_NAME': app_name,
        'SHIPPING_CHARGE': shipping_charge,
        'TAX_PERCENT': tax_percent,
    }

def cart_item_count(request):
    """
    Adds cart count for the current logged-in user to the context.
    """
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = cart.items.count()
        except Cart.DoesNotExist:
            count = 0
    else:
        count = 0

    return {'cart_item_count': count}