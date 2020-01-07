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
                request.session['user_name'] = user.user_name

                request.session['role'] = user.role_name.role_name
                request.session['menus'] = menus = user.role_name.get_menu_and_childmenu()

                return redirect(base)

    return render(request, 'login.html')


def logout(request):
    
    if 'uid' in request.session:
        del(request.session['uid'])
    if 'user_name' in request.session:
        del(request.session['user_name'])

    return render(request, 'login.html')



@user_required
def base(request, user):
    print('sss')
    return render(request, 'common/base.html')

@user_required
def modify(request, user):
    ctx={}
    
    if request.method == 'POST':

        action = request.POST.get('action','')
        if action == 'update':
            id = request.POST.get('id', '')

            r = AdminUser.objects.filter(id=id).first()
            _save_attr_(r, request)
            role = request.POST.get('role_name','')
            if role:
                role = Role.objects.filter(id=int(role)).first()
                r.role_name = role
                r.save()
            

    ctx['me'] =  user
    ctx['roles'] = roles = Role.objects.all()

    return render(request,'perModify.html',ctx)


def skin(request):
    return render(request, 'skin.html')
    

def index(request):
    
    return render(request, 'index.html')


def log(request):
    
    return render(request, 'log.html')


@page
def user(request):
    ctx = {}

    def op(r,request):
        _save_attr_(r, request)
        role = request.POST.get('user_role','')
        if role:
            r.role_name = Role.objects.filter(id=role).first()
            r.save()

    users = AdminUser.objects.exclude(status=-1).all()
    roles = Role.objects.all()

    if request.method == 'POST':
        action = request.POST.get('action','')
        if action == 'add':
            r = AdminUser()
            op(r,request)

        elif action == 'update':
            id = request.POST.get('id', '')
            r = AdminUser.objects.filter(id=id).first()
            op(r,request)

        elif action == 'delete':
            ids = request.POST.getlist('ids', '')
            u = AdminUser.objects.filter(id__in=ids).all()
            for item in u:
                item.status = -1
                item.save()
        elif action == 'validate':
            user_name = request.POST.get('user_name', '')
            id = request.POST.get('id','')
            if id:
                r = AdminUser.objects.filter(user_name=user_name.strip()).exclude(id=int(id))
            else:   
                r = AdminUser.objects.filter(user_name=user_name.strip())
            if r.exists():
                    return JsonResponse({'valid': False})

            return JsonResponse({'valid': True})

        elif action =='select':
            role = request.POST.get('role_name','')
            user = request.POST.get('user_name','')
            if role:
                users = users.filter(role_name__id=role).all()
            if user:
                users = users.filter(user_name__icontains=user)
            ctx['u'] = user
            ctx['r'] = int(role) if role else ''


    ctx['users'] = ctx['objects'] = users
    ctx['roles'] = roles

    return (ctx,'user.html')


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
    ctx['auth'] = r.get_auth_ids()
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


