from django.urls import path, include
from customer.views import dashboard, customer_order_history, customer_wish_lists, customer_account_settings, customer_addresses, password_change_view

urlpatterns = [
    path('dashboard/', dashboard, name='customer_dashboard'),
    path('order-history/', customer_order_history, name='customer_order_history'),
    path('wish-lists/', customer_wish_lists, name='customer_wish_lists'),
    path('addresses/', customer_addresses, name='customer_addresses'),
    path('account-settings/', customer_account_settings, name='customer_account_settings'),
    path('password-change/', password_change_view, name='customer_password_change'),
]