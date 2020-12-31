
from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        # elif request.user.is_authenticated==None:
        #     return redirect('login')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def allowed_users(allowed_roles=[]):
    def decorater(view_func):
        def wrapper_func(request, *args, **kwargs):
            group=None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return  HttpResponse("u r not authorized")
        return wrapper_func
    return decorater




def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        if group == 'customer':
            return redirect('home')
        elif group == 'admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('registerPage')
    return HttpResponse("404 error")

