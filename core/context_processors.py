from core.models import Category

def categories_processor(request):
    categories = Category.objects.filter(parent=None).order_by('pk').prefetch_related('subcategories')
    return {
        'header_categories': categories
    }
