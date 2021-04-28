from django.http import HttpResponse
from django.shortcuts import redirect


# add @unauthenticated_user to call function, set redirect to correct page. 

def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('')
        else:
            return view_function(request, *args, **kwargs)

    return wrapper_function


# add @allowed_users(allowed_roles=['admin', 'venues', 'users']) under @login_required(login_url='login')

def allowed_users(allowed_roles=[]):
    def decorator(view_function):
        def wrapper_function(request, *args, **kwargs):

            group = None
            if request.users.groups.exists():
                group = request.users.groups.all()[0].name
            
            if group in allowed_roles:
                return view_function(request, *args, **kwargs)

            else:
                return HttpResponse("That's a no from me dawg.")
        return wrapper_function
    return decorator



    