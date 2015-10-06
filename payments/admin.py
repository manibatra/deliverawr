from django.contrib import admin
from .models import UserPayment
from django.conf import settings
# Register your models here.

if settings.DEBUG:
	admin.site.register(UserPayment)