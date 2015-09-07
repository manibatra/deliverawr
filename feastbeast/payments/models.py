from django.db import models
from django.conf import settings

# Create your models here.
#extending the django default user model to store stripe info
class UserPayment(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	stripe_id = models.CharField(max_length=30)
