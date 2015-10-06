from django.contrib import admin
from .models import UserOrder, Detail

# Register your models here.
class UserOrderAdmin(admin.ModelAdmin):
	list_filter = ('restaurant',)

admin.site.register(UserOrder, UserOrderAdmin)
