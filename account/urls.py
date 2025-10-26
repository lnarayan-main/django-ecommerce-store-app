from django.urls import path, include
from account.views import home, login_view, register_view, password_reset, password_reset_confirm, activate_account, dashboard, password_change_view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activate/<str:uidb64>/<str:token>/', activate_account, name='activate_account'),
    path('password-reset/', password_reset, name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', password_reset_confirm, name='password_reset_confirm'),
    path('dashboard/', dashboard, name='dashboard'),
    path('password-change', password_change_view, name='password_change'),
]