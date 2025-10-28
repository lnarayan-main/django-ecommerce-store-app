from django.urls import path
from core.views import home, product_detail, products_by_category

urlpatterns = [
    path('', home, name='home'),
    path('product-detail/<int:product_id>', product_detail, name='product_detail'),
    path('products/<int:category_id>', products_by_category, name='products_by_category')
]