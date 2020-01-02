from django.shortcuts import render, redirect


import math
import datetime
import functools




def user_required(func):

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        from meta import api
        
        wrapper.__name__ = func.__name__

        token = request.session['token'] if 'token' in request.session else ''
        
        if not token:
            token = request.GET.get('token', '')
            if token:
                request.session['token'] = token

        next_url = request.get_full_path()

        if not token:
            return redirect('/login/public/account/?next=' + next_url)

        try:
            user =  api.check_token(token) #User.objects.first() 
        except APIError:
            return redirect('/login/public/account/?next=' + next_url)

        request.user = user
        result = func(request, user=user, *args, **kwargs)
        return result

    return wrapper


def now():
    return datetime.datetime.now()


def get_park_time(in_time, out_time=None):
    out_time =  out_time if out_time else now()
    diff = out_time - in_time
    hours = math.floor(diff.seconds / 3600)
    minutes = math.ceil((diff.seconds % 3600) / 60 )
    return hours, minutes
