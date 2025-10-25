from django.urls import path, include
from account.views import home, login, register, password_reset, password_reset_confirm, activate_account

urlpatterns = [
    path('', home, name='home'),
    path('login', login, name='login'),
    path('register', register, name='register'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate_account'),
    path('password-reset', password_reset, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
]