from django.shortcuts import render
from parkinglot.models import Worker
from administrator.models import AdminUser

# Create your views here.


#管理员登陆
def manage_login(request):	#username:管理员名字
	ctx = {}

	if request.method == 'POST':
		username = request.POST.get('account')	#user_name为html页面元素中name
		if not username:
			dic = {'msg':'请提交用户名'}
			return render(request,'manage_login.html',dic)

		password = request.POST.get('password')
		if not password:
			dic = {'msg':'请提交密码'}
			return render(request,'manage_login.html',dic)

		#查找用户
		user = AdminUser.objects.filter(user_name=username)

		#用户不存在
		if not user:
			dic = {'msg':'用户名或密码错误'}
			return render(request,'manage_login.html',dic)

		#密码不正确
		if user[0].user_pass != password:
			dic = {'msg':'用户名或密码错误'}
			return render(request,'manage_login.html',dic)

		#用户名和密码正确，存session进入首页
		request.session['username'] = username

		return render(request,'manage_home.html')


	return render(request,'manage_login.html',ctx)

#员工列表界面
def staff_list(request,parkinglot):	#哪一个停车场得从url中传过来，用来分辨是哪位
	ctx = {}

	if request.method == 'GET':
		workers_to_parkinglot = Worker.objects.filter(parkinglot=parkinglot)






	return render(request,'manage_login.html',ctx)


def manage_home(request):
	ctx = {}

	return render(request,'manage_home.html',ctx)
