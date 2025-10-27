from django.urls import path, include
from seller.views import dashboard, seller_order_history, seller_wish_lists, seller_addresses, seller_account_settings, password_change_view

urlpatterns = [
    path('dashboard/', dashboard, name='seller_dashboard'),
    path('order-history/', seller_order_history, name='seller_order_history'),
    path('wish-lists/', seller_wish_lists, name='seller_wish_lists'),
    path('addresses/', seller_addresses, name='seller_addresses'),
    path('account-settings/', seller_account_settings, name='seller_account_settings'),
    path('password-change/', password_change_view, name='seller_password_change'),
]