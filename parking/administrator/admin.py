from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(AdminUser)
admin.site.register(Role)
admin.site.register(Menu)
admin.site.register(Operation)
admin.site.register(Authority)
