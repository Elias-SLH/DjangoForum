from django.shortcuts import redirect


def unauthenticated_user(view_func):
    """Check if user is authenticated or not"""
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('qr:index')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func
