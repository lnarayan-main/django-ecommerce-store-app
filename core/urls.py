from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product-detail/<int:product_id>', views.product_detail, name='product_detail'),
    path('products/', views.products_listing, name='product_listing'),
    path('products/<int:category_id>', views.products_listing, name='products_by_category'),
    path('brand/<int:brand_id>/', views.products_listing, name='products_by_brand'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service, name='terms_of_service'),
    path('faq/', views.faq, name='faq'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
]