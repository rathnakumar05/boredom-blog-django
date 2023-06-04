from functools import wraps
from django.shortcuts import redirect

def anonymous_required(view_function):
    @wraps(view_function)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_function(request, *args, **kwargs)
    return wrapper

def verified_required(view_function):
    @wraps(view_function)
    def wrapper(request, *args, **kwargs):
        if not request.session['is_verified']:
            return redirect('send-verify-token')
        return view_function(request, *args, **kwargs)
    return wrapper

def not_verified(view_function):
    @wraps(view_function)
    def wrapper(request, *args, **kwargs):
        if request.session['is_verified']:
            return redirect('home')
        return view_function(request, *args, **kwargs)
    return wrapper