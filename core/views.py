from django.shortcuts import render, get_object_or_404
from seller.models import Product
from core.models import Category



def home(request):
    products = Product.objects.all()
    latest_products = Product.objects.order_by('-created_at')[:4]
    categories = Category.objects.filter(parent=None).all()
    context = {
        'products': products,
        'categories': categories,
        'latest_products': latest_products,
    }
    return render(request, 'account/home.html', context)


def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    latest_products = Product.objects.exclude(pk=product.id).order_by('-created_at')[:4]

    context = {
        'product': product,
        'latest_products': latest_products,
    }

    return render(request, 'core/product-details.html', context)