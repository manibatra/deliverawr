from django.db import models
from django.conf import settings

# Create your models here.
class Orders(models.Model):
	order_id = models.AutoField(primary_key=True)
	user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_order')
	restaurant = models.ForeignKey('restaurants.Restaurant', related_name='restaurant_order')
	menu_items = models.ManyToManyField('restaurants.MenuItem')
	total = models.DecimalField(max_digits=10, decimal_places=2)
	datetime = models.DateTimeField(auto_now_add=True)



