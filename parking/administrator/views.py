from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


from .models import *
from .decorators import page, _save_attr_
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .decorators import user_required
from django.shortcuts import redirect


'''系统设置模块'''

@csrf_exempt
def login(request):
    
    if request.method == 'POST':
        
        action = request.POST.get('action','')


        if action == 'login':
            user_name = request.POST.get('user_name')
            password = request.POST.get('user_pass')
            user = AdminUser.objects.filter(user_name=user_name,user_pass=password).first()
            if user :
                request.session['uid'] = user.id

                return render(request, 'base.html')
            else:
                return render(request, 'login.html')

        return render(request, 'base.html')

    return render(request, 'login.html')


# @user_required
def base(request):
    return render(request, 'base.html')

@user_required
def modify(request,me):
    ctx={}
    
    if request.method == 'POST':

        action = request.POST.get('action','')
        if action == 'update':
            id = request.POST.get('id', '')

            r = AdminUser.objects.filter(id=id)
            _save_attr_(r.first(), request)

            return redirect('/administrator/modify/')



    ctx['me'] =  me
    ctx['roles'] = roles = Role.objects.all()

    return render(request,'perModify.html',ctx)


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
            u = AdminUser.objects.filter(id__in=ids).all()
            for item in u:
                item.status = -1
                item.save()



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


