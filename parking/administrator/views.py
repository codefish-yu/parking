from django.shortcuts import render

# Create your views here.


from .models import Role
from .decorators import page
from django.http import JsonResponse


'''系统设置模块'''


def login(request):

    if request == 'POST':
        pass

        return render(request, 'base.html')

    return render(request, 'login.html')


def base(request):
    return render(request, 'base.html')


def skin(request):
    return render(request, 'skin.html')
    

def index(request):
    
    return render(request, 'index.html')


@page
def user(request):
    ctx = {}

    



    return render(request,'user.html')



@page
def role(request):
    ctx = {}

    roles = Role.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'add':
            r = Role()
            _save_attr_(r, request)

        elif action == 'update':
            id = request.POST.get('id', '')
            r = Role.objects.filter(id=id)
            _save_attr_(r.first(), request)

        elif action == 'search':
            ctx['role_name'] = role_name = request.POST.get('role_name', '')
            roles = Role.objects.filter(role_name__contains=role_name.strip())

        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            Role.objects.filter(id__in=ids).delete()

        elif action == 'validate':
            role_name = request.POST.get('role_name', '')
            id = request.POST.get('id', '')

            r = Role.objects.filter(role_name=role_name.strip())
            if r.exists():
                if id:
                    if r.first().id != int(id):
                        return JsonResponse({'valid': False})
                else:
                    return JsonResponse({'valid': False})

            return JsonResponse({'valid': True})

    ctx['objects'] = roles

    return (ctx, 'role.html')




def _save_attr_(obj,request):
    fields = obj._meta.fields

    for field in fields:
        field_name = field.name
        value = request.POST.get(field_name, '')
        print(field_name)
        print(value)
        if value:
            obj.__setattr__(field_name, value.strip())
        else:
            value = request.FILES.get(field_name, '')
            if value:
                obj.__setattr__(field_name, value)
    obj.save()



def d(url):
    path = url.split('Static/')
    path = path[1]
    dir = os.path.split(path)
    path = dir[0]
    file = dir[1]
    if not os.path.exists(path):
        os.mkdir(path)
    with open(path+'/'+file, 'w') as f:
        f.write(requests.get(url).text)
        f.flush()
        f.close()
