from django.shortcuts import render, get_object_or_404, redirect
from seller.models import Product, Size, Brand, Color
from core.models import Category, Order
from django.core.paginator import Paginator
from core.utils import get_sibling_categories
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.forms import NewsletterSubscriptionForm



def home(request):
    products = Product.objects.all()
    latest_products = Product.objects.order_by('-created_at')[:4]
    categories = Category.objects.filter(parent=None).order_by('pk').prefetch_related('subcategories')

    form = NewsletterSubscriptionForm()

    context = {
        'products': products,
        'categories': categories,
        'latest_products': latest_products,
        'form': form
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
    sort_by = request.GET.get('sort_by', 'latest')

    sort_mapping = {
        'latest': '-created_at',
        # 'popular': '-views',
        'popular': 'name',
        'a_z': 'name', 
    }

    products = Product.objects.filter(category_id=category_id)

    products = products.order_by(sort_mapping[sort_by])

    categories = Category.objects.filter(parent=None).order_by('pk').prefetch_related('subcategories')

    current_category = get_object_or_404(Category, pk=category_id)
   
    sibling_categories = get_sibling_categories(category_id)

    sizes = Size.objects.all()
    brands = Brand.objects.all()
    colors = Color.objects.all()

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    contenxt = {
        'products': page_obj,
        'categories': categories,
        'sizes': sizes,
        'brands': brands,
        'colors': colors,
        'sibling_categories': sibling_categories,
        'current_category': current_category,
    }

    return render(request, 'core/product-filters.html', contenxt)


def privacy_policy(request):
    return render(request, 'core/privacy-policy.html')

def terms_of_service(request):
    return render(request, 'core/terms-of-service.html')

def faq(request):
    return render(request, 'core/faq.html')


def subscribe_newsletter(request):
    if request.method == 'POST':
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            try:
                form.save() 
                messages.success(request, "Success! Check your email for a $50 discount code.")
            except Exception:
                messages.warning(request, "You are already subscribed to OpenBazaar.")
                
            return redirect('home')
    
    form = NewsletterSubscriptionForm()
    return {'form': form}