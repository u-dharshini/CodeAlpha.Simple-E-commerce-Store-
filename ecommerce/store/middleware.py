from django.shortcuts import redirect
from django.conf import settings

EXEMPT_URLS = [
    settings.LOGIN_URL.rstrip('/'),  # /login
    '/signup',
    '/logout',
    '/admin',
    '/static',
]

class LoginRequiredMiddleware:
    """Redirects unauthenticated users to login page except for exempt URLs."""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info.rstrip('/')
        if not request.user.is_authenticated:
            if not any(path.startswith(url) for url in EXEMPT_URLS):
                return redirect(settings.LOGIN_URL)
        return self.get_response(request)
