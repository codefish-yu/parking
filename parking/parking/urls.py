"""parking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from administrator import views as a
from car import views as car
from parkinglot import views as park

urlpatterns = [
    path('admin/', admin.site.urls),


    # administrator
    path('',a.base),
    path('login/',a.login),
    path('base/', a.base),   
    path('index/', a.index),
    path('administrator/role/', a.role),
    path('administrator/role/<int:id>/', a.get_role),
    path('administrator/user/',a.user),
    path('administrator/modify/',a.modify),
    # user


    # car 
    path('car/inner_car/', car.inner_car),
    


    
    #parkinglot
    path('parkinglot/parking_lot/',park.parking_lot,name='parking_lot'),
    path('parkinglot/worker/', park.worker),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
