from django.shortcuts import render
from restaurants.models import MenuItem

# Create your views here.

def detail(request, restaurant_id):

	menu_id = 23  #hardcoded for now, will be using restaurant_id to get the time of the day and accordingly the menu_id in the future
	all_items = MenuItem.objects.all()
	all_categories = MenuItem.objects.order_by('item_category').values('item_category').distinct()
	context = {'categories': all_categories, 'items': all_items}
	return render(request, 'restaurants/menu.html', context)

