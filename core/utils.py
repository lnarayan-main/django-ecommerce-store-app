from django.shortcuts import get_object_or_404
from core.models import Category

def get_sibling_categories(category_id):
    current_category = get_object_or_404(Category, pk=category_id)
    parent_id = current_category.parent_id 
    sibling_categories = Category.objects.filter(
        parent_id=parent_id
    #).exclude(
    #    pk=category_id
    ).order_by(
        'name'
    )
    
    return sibling_categories