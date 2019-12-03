from django.urls import path
from django.shortcuts import render,redirect
from .models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


import re
import json
import xlwt


def user_required(view_func):

    def wrapper(request, *args, **kwargs):
        if 'uid' not in request.session:
            return redirect('/login/')

        user = AdminUser.objects.filter(id=request.session['uid']).first()
        return view_func(request, me=user, *args, **kwargs)

    return wrapper


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


''' 小工具 ''' 
def _save_attr_(obj,request):
    fields = obj._meta.fields

    for field in fields:
        field_name = field.name
        value = request.POST.get(field_name, '')

        if value:
            if str(type(field)) == "<class 'django.db.models.fields.related.ForeignKey'>":
                pass
            else:
                obj.__setattr__(field_name, value.strip())
        else:
            value = request.FILES.get(field_name, '')
            if value:
                obj.__setattr__(field_name, value)
    
def export_excel(obj,name):
    e = xlwt.Workbook(encoding='utf-8')
    w = e.add_sheet(name)
    tip =0
    for i in obj._meta.fields:
        w.write(0,tip,i.verbose_name)
        tip += 1

    return w



  
