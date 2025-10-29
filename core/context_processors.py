from core.models import Category
import os
from django.conf import settings

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
    
    return {
        'APP_NAME': app_name,
    }
