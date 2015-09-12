from django.db import models
from django.conf import settings

# Create your models here.
#referencing the default user model to add multiple address related fields
class UserAddress(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	street_address = models.CharField(max_length=100)
	postcode = models.CharField(max_length=8)
	country = models.CharField(max_length=20)
	phone_no = models.CharField(max_length=15)
	default = models.BooleanField()



