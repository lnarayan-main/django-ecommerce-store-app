from django.urls import path, include
from customer.views import dashboard

urlpatterns = [
    path('dashboard/', dashboard, name='customer_dashboard'),
]