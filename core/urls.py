from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product-detail/<int:product_id>', views.product_detail, name='product_detail'),
    path('products/<int:category_id>', views.products_by_category, name='products_by_category'),
]