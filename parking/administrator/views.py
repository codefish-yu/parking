from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


from .models import *
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


# @page
def user(request):
    ctx = {}

    users = AdminUser.objects.all()
    roles = Role.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action','')
        if action == 'add':

            r = AdminUser()
            _save_attr_(r, request)
        elif action == 'update':
            id = request.POST.get('id', '')
            r = AdminUser.objects.filter(id=id)
            _save_attr_(r.first(), request)

        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            print(ids)
            AdminUser.objects.filter(id__in=ids).delete()



    ctx['users'] = users
    ctx['roles'] = roles

    return render(request,'user.html',ctx)


@csrf_exempt
@page
def role(request):
    ctx = {}

    roles = Role.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'add':
            r = Role()
            _save_attr_(r, request)

            save_auth(r, request)

        elif action == 'update':
            id = request.POST.get('id', '')

            r = Role.objects.filter(id=id).first()
            _save_attr_(r, request)
            save_auth(r, request)

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

    ctx['menus'] = Menu.objects.filter(parent=None).order_by('id')

    return (ctx, 'role.html')


@csrf_exempt
def get_role(request, id):
    ctx = {}

    ctx['role'] = r = Role.objects.filter(id=id).first()
    ctx['auth'] = r.get_auth()
    ctx['menus'] = Menu.objects.filter(parent=None).order_by('id')

    return render(request, 'edit_role.html', ctx)


def save_auth(r, request):
    menus = request.POST.getlist('menu', [])
    child_menus = request.POST.getlist('child_menu', [])
    operations = request.POST.getlist('operation', [])

    Authority.objects.filter(role=r).delete()

    for i in child_menus:
        child_menu = Menu.objects.filter(id=i).first()
        auth = Authority.objects.create(role=r, menu=child_menu.parent, child_menu=child_menu)
        ops = child_menu.operation.filter(id__in=operations)

        for j in ops:
            auth.operation.add(j)

    return


@page
def worker(request):
    ctx = {}

    workers = Worker.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action', '')
        if action == 'add':
            r = Worker()
            _save_attr_(r, request)


        elif action == 'update':
            id = request.POST.get('id', '')

            r = Worker.objects.filter(id=id).first()
            _save_attr_(r, request)
            save_auth(r, request)

        elif action == 'search':
            ctx['worker_name'] = worker_name = request.POST.get('worker_name', '')
            roles = Worker.objects.filter(worker_name__contains=worker_name.strip())

        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            Worker.objects.filter(id__in=ids).delete()

        elif action == 'validate':
            number = request.POST.get('number', '')
            id = request.POST.get('id', '')

            r = Worker.objects.filter(number=number.strip())
            if r.exists():
                if id:
                    if r.first().id != int(id):
                        return JsonResponse({'valid': False})
                else:
                    return JsonResponse({'valid': False})

            return JsonResponse({'valid': True})

    ctx['objects'] = workers

    return (ctx, 'worker.html')



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


