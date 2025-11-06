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

    brands = Brand.objects.all()

    form = NewsletterSubscriptionForm()

    context = {
        'products': products,
        'categories': categories,
        'latest_products': latest_products,
        'form': form,
        'brands': brands,
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


def products_listing(request, category_id=None, brand_id=None):
    sort_by = request.GET.get('sort_by', 'latest')
    sort_mapping = {
        'latest': '-created_at',
        # 'popular': '-views', 
        'popular': 'name', 
        'a_z': 'name',
    }
    
    products = Product.objects.all()
    current_category = None
    current_brand = None
    sibling_categories = None
    
    if category_id:
        current_category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=current_category)
        sibling_categories = Category.objects.filter(parent=current_category.parent)
    elif brand_id:
        current_brand = get_object_or_404(Brand, id=brand_id)
        products = products.filter(brand=current_brand)
    
    category_filter = request.GET.getlist('category')
    size_filter = request.GET.getlist('size')
    brand_filter = request.GET.getlist('brand')
    color_filter = request.GET.getlist('color')
    
    if category_filter:
        products = products.filter(category_id__in=category_filter)
    
    if size_filter:
        products = products.filter(available_sizes__id__in=size_filter).distinct()
    
    if brand_filter:
        products = products.filter(brand_id__in=brand_filter).distinct()
    
    if color_filter:
        products = products.filter(available_colors__id__in=color_filter).distinct()
    
    products = products.order_by(sort_mapping.get(sort_by, '-created_at'))
    
    products = products.select_related('category', 'brand').prefetch_related(
        'available_sizes', 
        'available_colors', 
        'images'
    )
    
    sizes = Size.objects.all()
    brands = Brand.objects.all()
    colors = Color.objects.all()
    
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    query_params = request.GET.copy()
    if 'page' in query_params:
        query_params.pop('page')
    query_string = query_params.urlencode()
    
    context = {
        'products': page_obj,
        'current_category': current_category,
        'current_brand': current_brand,
        'sibling_categories': sibling_categories,
        'sizes': sizes,
        'brands': brands,
        'colors': colors,
        'selected_sizes': size_filter,
        'selected_brands': brand_filter,
        'selected_colors': color_filter,
        'selected_categories': category_filter,
        'query_string': query_string,  
    }
    
    return render(request, 'core/product-filters.html', context)



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