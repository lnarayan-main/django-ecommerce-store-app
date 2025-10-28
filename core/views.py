from django.shortcuts import render, get_object_or_404
from seller.models import Product
from core.models import Category
from django.core.paginator import Paginator



def home(request):
    products = Product.objects.all()
    latest_products = Product.objects.order_by('-created_at')[:4]
    categories = Category.objects.filter(parent=None).order_by('pk').prefetch_related('subcategories')
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


def products_by_category(request, category_id):
    products = Product.objects.filter(category_id=category_id).order_by('-created_at')

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    contenxt = {
        'products': page_obj,
    }


    return render(request, 'core/product-filters.html', contenxt)