from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='customer_dashboard'),
    path('order-history/', views.customer_order_history, name='customer_order_history'),
    path('wish-lists/', views.customer_wish_lists, name='customer_wish_lists'),
    path('addresses/', views.customer_addresses, name='customer_addresses'),
    path('addresses/<int:address_id>/', views.customer_addresses, name='customer_addresse_edit'),
    path('delete-address/<int:address_id>/', views.delete_address, name='customer_delete_address'),
    path('account-settings/', views.customer_account_settings, name='customer_account_settings'),
    path('password-change/', views.password_change_view, name='customer_password_change'),
    path('order-details/<int:order_id>/', views.order_details, name='customer_order_details'),
]