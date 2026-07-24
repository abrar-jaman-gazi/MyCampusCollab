from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect


class SuspendedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.is_suspended:
            logout(request)
            messages.error(request, 'Your account has been suspended. Contact an administrator.')
            return redirect('accounts:login')
        return self.get_response(request)
