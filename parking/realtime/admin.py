from django.contrib import admin

# Register your models here.

from .models import * 

admin.site.register(Bill)
admin.site.register(InAndOut)
admin.site.register(OpeningOrder)
admin.site.register(ExceptRecord)