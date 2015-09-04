from django.db import models

# Create your models here.
class MenuItem(models.Model):
	item_id = models.AutoField(primary_key=True)
	menu_id = models.IntegerField() #becomes a forein key later
	item_name = models.CharField(max_length=30)
	item_price = models.IntegerField()
	item_description = models.CharField(max_length=140)
	item_category = models.CharField(max_length=30)