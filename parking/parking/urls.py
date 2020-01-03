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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


from administrator import views as a
from car import views as car
from device import views as device
from parkinglot import views as park
from company import views as com
from wechat import views as wechat
from chargerule import views as charge
from realtime import views as realtime
from account import views as ac
from business import views as b


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('meta.urls')),


    # administrator
    path('',a.base),
    path('administrator/login/',a.login),
    path('administrator/logout/',a.logout),
    path('base/', a.base),   
    path('index/', a.index),
    path('administrator/log/', a.log),
    path('administrator/role/', a.role),
    path('administrator/role/<int:id>/', a.get_role),
    path('administrator/user/',a.user),
    path('administrator/modify/',a.modify),
    

    # user



    # car 
    path('car/inner_car/', car.inner_car),  
    

    # parkinglot

    path('parkinglot/parking_lot/',park.parking_lot),
    path('parkinglot/gate/',park.gate),
    path('parkinglot/worker/', park.worker),
    path('parkinglot/zone/',park.zone),
    path('parkinglot/place/',park.place),
    path('parkinglot/calendar/',park.calendar),



    # company

    path('company/company/',com.company),



    # device

    path('device/brake/',device.brake),
    path('device/camera/',device.camera),
    path('device/groundsensor/',device.groundsensor),



    # chargerule

    path('chargerule/baserule/',charge.base_rule),
    path('chargerule/card/',charge.card),
    path('chargerule/coupon/',charge.coupon),
    path('chargerule/cardtype/',charge.card_type),
    path('chargerule/coupontype/',charge.coupon_type),
    path('chargerule/chargedemo/',charge.chargedemo),
    path('chargerule/check_coupon/',charge.check_coupon),


    # realtime

    path('realtime/parkin/',realtime.parkin),
    path('realtime/in_out/',realtime.in_out),
    path('realtime/bill/',realtime.bill),


    # wechat
    path('wechat/parkin/<int:parkinglot_id>/<int:gate_id>/',wechat.parkin),
    path('wechat/parkout/<int:parkinglot_id>/<int:gate_id>/',wechat.parkout),
    path('wechat/parkout/<int:parkinglot_id>/',wechat.parkout),
    path('wechat/personal/mybill/<int:id>/',wechat.mybill),
    path('wechat/personal/mybill/',wechat.mybill),
    path('wechat/personal/mycard/',wechat.mycard),
    path('wechat/personal/mycoupon/',wechat.mycoupon),
    path('wechat/personal/myplate/bound/',wechat.bound),
    path('wechat/personal/myplate/',wechat.myplate),
    path('wechat/personal/',wechat.personal),
    path('wechat/problem/',wechat.problem),
    path('wechat/scan/coupon/<int:id>/<str:code>/',wechat.scan_coupon),


    #account
    path('account/spec_pass/',ac.spec_pass),
    path('account/correct/',ac.correct),
    path('account/record/',ac.record),
    path('account/personal/',ac.personal,name='personal'),
    path('account/begin_work/',ac.begin_work),


    #business
    path('business/com_login/',b.com_login),
    path('business/apply/<int:tc_id>/',b.apply),
    path('business/grant/',b.grant),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




