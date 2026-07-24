from functools import wraps
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def admin_required(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not (request.user.is_superuser or request.user.role == 'admin'):
            messages.error(request, 'Administrator access is required.')
            return redirect('dashboard:home')
        return view_func(request, *args, **kwargs)
    return wrapper
