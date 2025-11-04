from django.contrib.auth.decorators import login_required as django_login_required
from django.contrib.auth.views import redirect_to_login
from functools import wraps
from django.http import HttpResponseForbidden
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect

error_403_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>403 Forbidden - Access Denied</title>
        <!-- Load Tailwind CSS via CDN -->
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            /* Custom colors, matching your primary color */
            :root {
                --color-primary: #FF4466;
                --color-primary-dark: #cc3751;
            }
            .bg-primary-500 { background-color: var(--color-primary); }
            .text-primary-500 { color: var(--color-primary); }
            r".hover\:bg-primary-600:hover" { background-color: var(--color-primary-dark); }
            
            /* Ensure the body fills the viewport height */
            body { min-height: 100vh; }
        </style>
    </head>
    <body class="bg-gray-50 flex items-center justify-center p-4">

        <div class="max-w-md w-full text-center bg-white p-10 rounded-2xl shadow-xl border border-gray-200">
            <!-- Error Code -->
            <p class="text-7xl font-extrabold text-primary-500 mb-4">
                403
            </p>
            
            <!-- Error Title -->
            <h1 class="text-3xl font-bold text-gray-800 mb-4">
                Access Denied
            </h1>
            
            <!-- Error Message -->
            <p class="text-gray-600 mb-8">
                It looks like you don't have permission to view this page. This resource is restricted to authorized users only.
            </p>

            <!-- Call to Action Buttons -->
            <div class="flex flex-col space-y-4">
                <!-- Go Home Button -->
                <a href="/" class="bg-primary-500 text-white font-semibold py-3 px-6 rounded-full transition hover:bg-primary-600 shadow-lg">
                    Go to Homepage
                </a>
            </div>
            
            <p class="text-sm text-gray-400 mt-8">
                If you believe this is an error, please contact support.
            </p>
        </div>

    </body>
    </html>

    """

def login_and_role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        @django_login_required
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if required_role == "customer" and not user.is_customer:
                return HttpResponseForbidden(error_403_html)
            if required_role == "seller" and not user.is_seller:
                return HttpResponseForbidden(error_403_html)
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator



def custom_login_required(view_func):
    """
    Handles authentication for both normal and AJAX/fetch requests.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)

        # ✅ Normalize headers for fetch()
        requested_with = request.headers.get('X-Requested-With', '').lower()
        accept_header = request.headers.get('Accept', '').lower()

        is_ajax = (
            requested_with == 'xmlhttprequest'
            or 'application/json' in accept_header
        )

        if is_ajax:
            return JsonResponse({'error': 'Authentication required.'}, status=401)

        # Normal browser request → redirect to login
        return redirect_to_login(request.get_full_path())

    return _wrapped_view

