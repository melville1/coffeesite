from django.contrib import admin 
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register([Product,Order,Tag,OrderItem,Guest])
admin.site.register(Addressee, UserAdmin)
