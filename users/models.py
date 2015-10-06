from django.db import models
from django.conf import settings
import uuid

# Create your models here.
#referencing the default user model to add multiple address related fields
class UserAddress(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	street_address = models.CharField(max_length=100)
	city = models.CharField(max_length=20)
	postcode = models.CharField(max_length=8)
	country = models.CharField(max_length=20)
	default = models.BooleanField()

	def save(self, *args, **kwargs):
		if self.default:
			try:
				temp = UserAddress.objects.get(default=True, user=self.user)
				if self != temp:
					temp.default = False
					temp.save()
			except UserAddress.DoesNotExist:
				pass
		super(UserAddress, self).save(*args, **kwargs)

	def __str__(self):
		           # __unicode__ on Python 2
		return (self.street_address + ", " + self.city + " - " + self.postcode)

#model for saving the phone no of the user
class UserPhoneNo(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	phone_no = models.CharField(max_length=15)

	def __str__(self):
		           # __unicode__ on Python 2
		return (self.phone_no)

#model to save the user verification code
class UserVerification(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	ver_code = models.CharField(max_length=32)
