from django.shortcuts import render
from core.decorators import login_and_role_required

@login_and_role_required("customer")
def dashboard(request):
    return render(request, 'customer/dashboard.html')
