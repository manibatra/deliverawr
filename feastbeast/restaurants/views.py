from django.shortcuts import render
from django.http import HttpResponse
from restaurants.models import MenuItem
from carton.cart import Cart


# Create your views here.

def detail(request, restaurant_id):

	menu_id = 23  #hardcoded for now, will be using restaurant_id to get the time of the day and accordingly the menu_id in the future
	all_items = MenuItem.objects.all()
	all_categories = MenuItem.objects.order_by('item_category').values('item_category').distinct()
	context = {'categories': all_categories, 'items': all_items}
	return render(request, 'restaurants/menu.html', context)


def add(request, restaurant_id, item_id):
	cart = Cart(request.session)
	if request.is_ajax() or request.method == 'GET':
		#item_id = request.GET['item_id']
		product = MenuItem.objects.get(pk=item_id)
		cart.add(product, price=product.item_price)
		return HttpResponse(str(cart.total))
	else:
		return HttpResponse("Not Added")