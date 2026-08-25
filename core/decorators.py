from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in with administrator credentials.")
            return redirect('admin_login')
        if not request.user.is_admin_user():
            messages.error(request, "Access restricted. Administrator privileges required.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def driver_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to access your driver portal.")
            return redirect('login')
        if not (request.user.is_driver_user() or request.user.is_admin_user()):
            messages.error(request, "Access restricted. Driver portal is for registered drivers.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def passenger_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in or register as a passenger.")
            return redirect('login')
        if not (request.user.is_passenger_user() or request.user.is_admin_user()):
            messages.error(request, "Access restricted. Passenger account required.")
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def verified_driver_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in to access your driver portal.")
            return redirect('driver_login')
        if not (request.user.is_driver_user() or request.user.is_admin_user()):
            messages.error(request, "Access restricted. Driver portal is for registered drivers.")
            return redirect('home')
        driver = getattr(request.user, 'driver_profile', None)
        if driver and not driver.is_verified():
            messages.warning(request, "Your Driver KYC is currently pending administrator verification. Core services remain locked until approved.")
            return redirect('driver_dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
