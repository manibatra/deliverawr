from django.shortcuts import render
from django.http import HttpResponse
from restaurants.models import MenuItem
from carton.cart import Cart
from .models import Restaurant


# Create your views here.

def detail(request, restaurant_id):

	all_items = MenuItem.objects.filter(restaurant=restaurant_id)
	restaurant = Restaurant.get(pk=restaurant_id)
	all_categories = MenuItem.objects.order_by('category').values('category').distinct()
	context = {'categories': all_categories, 'items': all_items, 'restaurant': restaurant }
	return render(request, 'restaurants/menu.html', context)


def add(request, restaurant_id, item_id):
	cart = Cart(request.session)
	if request.is_ajax() or request.method == 'GET':
		#item_id = request.GET['item_id']
		product = MenuItem.objects.get(pk=item_id)
		cart.add(product, price=product.price)
		return HttpResponse(str(cart.total))
	else:
		return HttpResponse("Not Added")