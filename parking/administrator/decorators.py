from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from django.http import JsonResponse
from .urls import urlpatterns

# from .models import Token

import re
import json


def user_required(func):
    pass

    

def api(func):
    print('sdfsdf')
    @csrf_exempt
    def django_view(request):

        try:
            content = request.body
            
            if isinstance(content, bytes):
                params = json.loads(request.body.decode('utf8'))
            else:
                params = json.loads(request.body)

        except Exception as e:
            print(e)
            return JsonResponse({'code': -1, 'msg': '参数格式错误'})

        try:
            result = func(**params)
            if 'code' not in result:
                result = {'code': 0, 'result': result}
            return JsonResponse(result)

        except TypeError as e:
            print(e)
            a = re.findall(r'missing 1 required positional argument: \'(.*)\'', str(e))
            if a:
                return JsonResponse({'code': -1, 'msg': '缺少参数%s'% a[0]})
            else:
                return JsonResponse({'code': -1, 'msg': '参数有误'})

    name = func.__name__

    urlpatterns.append(path('api/%s/' % name, django_view))
    print(urlpatterns)




