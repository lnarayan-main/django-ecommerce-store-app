from django.urls import path
from core.views import home, product_detail

urlpatterns = [
    path('', home, name='home'),
    path('product-detail/<int:product_id>', product_detail, name='product_detail'),
]