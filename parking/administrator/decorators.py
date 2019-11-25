from django.urls import path
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


import re
import json


def user_required(func):
    pass


'''分页查询'''
def page(func):
    def view(request, *args, **kwargs):
        
        pagesize = int(request.POST.get('pagesize','10'))
        page = int(request.POST.get('page','1'))
        
        result = func(request, *args, **kwargs)

        if isinstance(result, tuple):
             
            res = result[0]
            res['pagesize'] = pagesize
            res['page'] = page
             
            paginator = Paginator(res['objects'], pagesize) 
            try:
                res['objects'] = paginator.page(page)
            except EmptyPage:
                res['objects'] = paginator.page(paginator.num_pages) 
            return render(request, result[1], res)

        elif isinstance(result, JsonResponse):
            return result

    view.__name__ = func.__name__

    return view

