from django.db import models


# Create your models here.
#model for the restaurant
class Restaurant(models.Model):
	restaurant_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=70)
	street_address = models.CharField(max_length=100)
	postcode = models.CharField(max_length=8)
	country = models.CharField(max_length=20)
	phone_no = models.CharField(max_length=15)
	primary_image = models.ImageField(upload_to='restaurants/primary_image/')
	secondary_image = models.ImageField(upload_to='restaurants/secondary_image/')

	def __str__(self):              # __unicode__ on Python 2
		return self.name

	def is_open(self):
		import datetime
		now = datetime.datetime.now()
		current_day = now.strftime("%A")
		delivery_hours = DeliveryHours.objects.get(restaurant=self, day=current_day[:2])
		open_hour = delivery_hours.open_hour
		close_hour = delivery_hours.close_hour
		time = datetime.datetime.now().time()
		if(time >= open_hour and time < close_hour):
			return True
		else:
			return False

	def opening_time(self):
		import datetime
		now = datetime.datetime.now()
		current_day = now.strftime("%A")
		delivery_hours = DeliveryHours.objects.get(restaurant=self, day=current_day[:2])
		open_hour = delivery_hours.open_hour
		return open_hour

	def closing_time(self):
		import datetime
		now = datetime.datetime.now()
		current_day = now.strftime("%A")
		delivery_hours = DeliveryHours.objects.get(restaurant=self, day=current_day[:2])
		close_hour = delivery_hours.close_hour
		return close_hour



#model for the restaurant delivery locations
class DeliveryLocation(models.Model):
	restaurant = models.ForeignKey('restaurants.Restaurant')
	postcode = models.CharField(max_length=8)

#model for the restaurant operating hours
class DeliveryHours(models.Model):
	MONDAY = 'Mo'
	TUESDAY = 'Tu'
	WEDNESDAY = 'We'
	THURSDAY = 'Th'
	FRIDAY = 'Fr'
	SATURDAY = 'Sa'
	SUNDAY = 'Su'

	DAYS = (
			  (MONDAY, 'Monday'),
			  (TUESDAY, 'Tuesday'),
			  (WEDNESDAY, 'Wednesday'),
			  (THURSDAY, 'Thursday'),
			  (FRIDAY, 'Friday'),
			  (SATURDAY, 'Saturday'),
			  (SUNDAY, 'Sunday'),
			)

	restaurant = models.ForeignKey('restaurants.Restaurant')
	day = models.CharField(max_length=2, choices=DAYS)
	open_hour = models.TimeField()
	close_hour = models.TimeField()

#model for the menu items in the restaurant
class MenuItem(models.Model):
	item_id = models.AutoField(primary_key=True)
	restaurant = models.ForeignKey('restaurants.Restaurant', related_name='menu_items')
	name = models.CharField(max_length=30)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	description = models.CharField(max_length=140, blank=True)
	category = models.CharField(max_length=30, blank=True)
	time_available = models.CharField(max_length=15, blank=True)
	option = models.ForeignKey('self', blank=True, related_name='has_options', null=True)
	option_category = models.CharField(max_length=30, blank=True)
	ingredient = models.BooleanField()
	add_on = models.BooleanField()
	removable = models.BooleanField()
	choose_one = models.BooleanField()

	def __str__(self):
		if self.option:              # __unicode__ on Python 2
			return (self.name + " - " + self.option.name)
		else:
			return self.name




