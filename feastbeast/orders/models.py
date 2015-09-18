from django.db import models
from django.conf import settings

# Create your models here.
class Orders(models.Model):
	order = models.ForeignKey('OrderStatus', related_name='order')
	restaurant = models.ForeignKey('restaurants.Restaurant', related_name='restaurant_order')
	total = models.DecimalField(max_digits=10, decimal_places=2)
	completed_datetime = models.DateTimeField(auto_now_add=True)

class OrderDetail(models.Model):
	order = models.ForeignKey('OrderStatus', related_name='order_number')
	menu_item = models.ForeignKey('restaurants.MenuItem', related_name='menu_item')
	add_ons = models.ManyToManyField('restaurants.MenuItem', related_name='add_ons')
	removed = models.ManyToManyField('restaurants.MenuItem', related_name='removed_items')

class OrderStatus(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	is_completed = models.BooleanField()

