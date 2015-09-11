from django.shortcuts import render
from django.http import HttpResponse

from carton.cart import Cart

#gettting various models required for passing info to the view
from .models import Restaurant
from payments.models import UserPayment
from users.models import UserAddress
from restaurants.models import MenuItem

import stripe

stripe.api_key = "sk_test_Qt90eBDjHDIYHCO0YREdeEGk"


# Create your views here.

def detail(request, restaurant_id):

	all_items = MenuItem.objects.filter(restaurant=restaurant_id)
	restaurant = Restaurant.objects.get(pk=restaurant_id)
	all_categories = MenuItem.objects.order_by('category').values('category').distinct()
	context = {'categories': all_categories, 'items': all_items, 'restaurant': restaurant }

	#getting the stored user payment info
	user_payment_info = UserPayment.objects.filter(user=request.user)
	if len(user_payment_info) > 0:
		context['payment_info'] = 'true'
		#retrieving the customer info from stripe
		customer = stripe.Customer.retrieve(user_payment_info[0].stripe_id)
		#retreving and sending the last4 digits and brand of the default card to the template
		default_card = customer.sources.retrieve(customer['default_source'])
		context['brand'] = default_card['brand']
		context['last4'] = default_card['last4']
		#setting the list of cards and brand names
		user_payment_methods = []
		for card_object in customer['sources']['data']:
			payment_method = {}
			payment_method['brand'] = card_object['brand']
			payment_method['last4'] = card_object['last4']
			user_payment_methods.append(payment_method)

		context['user_payment_methods'] = user_payment_methods

	else:
		context['payment_info'] = 'false'


	#getting user address info
	user_address_info = UserAddress.objects.filter(user=request.user)
	if len(user_address_info) > 0:
		context['delivery_info'] = 'true'
		#retrieving the user address object
		current_user = user_address_info[0]

		context['street_address'] = current_user.street_address
		context['user_addresses'] = user_address_info
		context['country'] = current_user.country
	else:
		context['delivery_info'] = 'false'


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