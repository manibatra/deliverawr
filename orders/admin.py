from django.contrib import admin
from .models import UserOrder, Detail

# Register your models here.
class DetailInline(admin.TabularInline):
	model = Detail
	extra = 0

	def get_readonly_fields(self, request, obj=None):
		if obj: # editing an existing object
			return self.readonly_fields + ('menu_item', 'add_ons', 'removed', 'subtotal')
		return self.readonly_fields

class UserOrderAdmin(admin.ModelAdmin):
	list_filter = ('restaurant',)
	inlines = [DetailInline,]

	def get_readonly_fields(self, request, obj=None):
		if obj: # editing an existing object
			return self.readonly_fields + ('user', 'restaurant', 'order_time', 'total_price', 'delivery_address', 'phone_no')
		return self.readonly_fields

admin.site.register(UserOrder, UserOrderAdmin)
