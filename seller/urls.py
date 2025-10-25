from django.urls import path, include
from seller.views import dashboard

urlpatterns = [
    path('dashboard/', dashboard, name='seller_dashboard'),
]