from django.contrib import admin
from .models import UserAddress, UserPhoneNo

# Register your models here.
admin.site.register(UserAddress)
admin.site.register(UserPhoneNo)
