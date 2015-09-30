from django.db import models
from django.conf import settings



class UserOrder(models.Model):
	order_id = models.AutoField(primary_key=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='ordered_by')
	restaurant = models.ForeignKey('restaurants.Restaurant', related_name='ordered_from')
	order_time = models.DateTimeField(auto_now_add=True)
	total_price = models.DecimalField(max_digits=10, decimal_places=2)
	delivery_address = models.ForeignKey('users.UserAddress', related_name='delivered_to')

class Detail(models.Model):
	order = models.ForeignKey('UserOrder', related_name='order_number')
	menu_item = models.ForeignKey('restaurants.MenuItem', related_name='menu_item')
	add_ons = models.ManyToManyField('restaurants.MenuItem', related_name='added_items')
	removed = models.ManyToManyField('restaurants.MenuItem', related_name='removed_items')
	subtotal = models.DecimalField(max_digits=10, decimal_places=2)