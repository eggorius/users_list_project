from django.http import HttpResponse


def check_for_blocked_users(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.groups.exists():
            group = request.user.groups.all()[0]
            if group.name == 'blocked':
                return HttpResponse('UPS! You are blocked!<br> <a href=\"/login\">Log in</a>')
        return view_func(request, *args, **kwargs)
    return wrapper_func

