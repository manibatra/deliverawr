from django.contrib import admin
from .models import Restaurant, DeliveryLocation, MenuItem, DeliveryHours, Options

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(DeliveryLocation)
admin.site.register(MenuItem)
admin.site.register(DeliveryHours)
admin.site.register(Options)
