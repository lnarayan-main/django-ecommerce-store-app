from django.urls import path, include
from seller.views import dashboard, seller_order_history, seller_wish_lists, seller_addresses, seller_account_settings, password_change_view, products_list, create_product, product_edit, product_delete

urlpatterns = [
    path('dashboard/', dashboard, name='seller_dashboard'),
    path('order-history/', seller_order_history, name='seller_order_history'),
    path('wish-lists/', seller_wish_lists, name='seller_wish_lists'),
    path('addresses/', seller_addresses, name='seller_addresses'),
    path('account-settings/', seller_account_settings, name='seller_account_settings'),
    path('password-change/', password_change_view, name='seller_password_change'),
    path('create-product/', create_product, name='product_create'),
    path('edit-product/<int:product_id>/:', product_edit, name='product_edit'),
    path('delete-product/<int:product_id>/', product_delete, name='product_delete'),
    path('products-list/', products_list, name='products_list'),
]