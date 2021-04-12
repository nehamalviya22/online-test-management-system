from django.shortcuts import redirect
from .models import Admin

def admin_is_logged_in(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return redirect('AdminLogin')
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap