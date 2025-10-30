from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='seller_dashboard'),
    path('order-history/', views.seller_order_history, name='seller_order_history'),
    path('wish-lists/', views.seller_wish_lists, name='seller_wish_lists'),
    path('addresses/', views.seller_addresses, name='seller_addresses'),
    path('addresses/<int:address_id>/', views.seller_addresses, name='seller_addresse_edit'),
    path('delete-address/<int:address_id>/', views.delete_address, name='delete_address'),
    path('account-settings/', views.seller_account_settings, name='seller_account_settings'),
    path('password-change/', views.password_change_view, name='seller_password_change'),
    path('create-product/', views.create_product, name='product_create'),
    path('edit-product/<int:product_id>/', views.product_edit, name='product_edit'),
    path('products/<int:image_id>/delete-image/', views.delete_product_image, name='delete_product_image'),
    path('delete-product/<int:product_id>/', views.product_delete, name='product_delete'),
    path('products-list/', views.products_list, name='products_list'),
]