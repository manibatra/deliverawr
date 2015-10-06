from django.contrib import admin
from .models import UserAddress, UserPhoneNo
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import Group



# Register your models here.
admin.site.unregister(Group)

if settings.DEBUG:
	admin.site.register(UserAddress)
	admin.site.register(UserPhoneNo)
else:
	admin.site.unregister(User)
