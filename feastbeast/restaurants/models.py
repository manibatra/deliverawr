from django.db import models

# Create your models here.
#model for the restaurant
class Restaurant(models.Model):
	restaurant_id = models.AutoField(primary_key=True)
	name = models.CharField(max_lenth=70)
	address = models.CharField(max_lenth=100)

#model for the restaurant delivery locations
class DeliveryLocation(models.Model):
	restaurant = models.ForeignKey('Restaurant')
	postcode = models.CharField(max_length=8)

#model for the restaurant operating hours
class DeliveryHours(models.Model):
	DAYS = [
			  (1, _("Monday")),
			  (2, _("Tuesday")),
			  (3, _("Wednesday")),
			  (4, _("Thursday")),
			  (5, _("Friday")),
			  (6, _("Saturday")),
			  (7, _("Sunday")),
			]

	restaurant = models.ForeignKey('Restaurant')
	day = models.IntegerField(choices=DAYS, unique=True)
	open_hour = models.TimeField()
	close_hour = models.TimeField()

#model for the menu items in the restaurant
class MenuItem(models.Model):
	item_id = models.AutoField(primary_key=True)
	restaurant = models.ForeignKey('Restaurant')
	name = models.CharField(max_length=30)
	price = models.DecimalField(max_digits=3, decimal_places=2)
	description = models.CharField(max_length=140)
	category = models.CharField(max_length=30)
	time_available = models.CharField(max_length=15)

#model for the options available to add and remove from the menu item
class Options(models.Model):
	item = models.ForeignKey('MenuItem')
	name = models.CharField(max_length=35)
	ingredient = models.BooleanField()
	add_on = models.BooleanField()
	removable = models.BooleanField()
	price = models.DecimalField(max_digits=3, decimal_places=2)
