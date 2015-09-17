from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers

from carton.cart import Cart

#gettting various models required for passing info to the view
from .models import Restaurant
from payments.models import UserPayment
from users.models import UserAddress
from restaurants.models import MenuItem

import stripe
import json

stripe.api_key = "sk_test_Qt90eBDjHDIYHCO0YREdeEGk"


# Create your views here.
#returns the menu info, stripe_id, default address if any, default card info
def detail(request, restaurant_id):

	#sending the menu objects
	all_items = MenuItem.objects.exclude(category__exact='').filter(restaurant=restaurant_id)
	restaurant = Restaurant.objects.get(pk=restaurant_id)
	all_categories = MenuItem.objects.filter(restaurant=restaurant_id).exclude(category__exact='').order_by('category').values('category').distinct()
	context = {'categories': all_categories, 'items': all_items, 'restaurant': restaurant }

	#getting the stored user payment info
	user_payment_info = UserPayment.objects.filter(user=request.user)
	if len(user_payment_info) > 0:
		context['payment_info'] = 'true'
		#retrieving the customer info from stripe
		stripe_id = user_payment_info[0].stripe_id
		customer = stripe.Customer.retrieve(stripe_id)
		context['stripe_id'] = stripe_id
		default_card_id = customer.default_source
		#have to put this whole thing under an additional check to see if there are any cards associated with this customer
		#retreving and sending the last4 digits and brand of the default card to the template
		if default_card_id is None:
			context['payment_info'] = 'false'
		else:
			default_card = customer.sources.retrieve(default_card_id)
			context['brand'] = default_card['brand']
			context['last4'] = default_card['last4']


		#setting the list of cards and brand names
		# user_payment_methods = []
		# for card_object in customer['sources']['data']:
		# 	payment_method = {}
		# 	payment_method['brand'] = card_object['brand']
		# 	payment_method['last4'] = card_object['last4']
		# 	user_payment_methods.append(payment_method)

		# context['user_payment_methods'] = user_payment_methods

	else:
		context['payment_info'] = 'false'


	#getting user  default address info
	user_address_info = UserAddress.objects.filter(user=request.user, default=True)
	if len(user_address_info) > 0:
		context['delivery_info'] = 'true'
		#retrieving the user address object
		current_user = user_address_info[0]
		context['street_address'] = current_user.street_address
		context['country'] = current_user.country
	else:
		context['delivery_info'] = 'false'


	return render(request, 'restaurants/menu.html', context)

#function to add the product to the cart
def add(request, restaurant_id, item_id):
	cart = Cart(request.session)
	if request.is_ajax() or request.method == 'GET':
		#item_id = request.GET['item_id']
		product = MenuItem.objects.get(pk=item_id)
		cart.add(product, price=product.price)
		return HttpResponse(str(cart.total))
	else:
		return HttpResponse("Not Added")

#function to add  product and its custom options to the cart
def addCustom(request):
	cart = Cart(request.session)
	if request.is_ajax() or request.method == 'GET':
		#item_id = request.GET['item_id']
		items_to_add = json.loads(request.GET['data'])
		for item in items_to_add:
			product = MenuItem.objects.get(pk=item['item_id'])
			cart.add(product, price=product.price)
		return HttpResponse(str(cart.total))
	else:
		return HttpResponse("Not Added")

def customOptions(request):
	item_id = request.GET['item_id']
	all_options = MenuItem.objects.exclude(option_category__exact='').filter(option=item_id)
	all_option_categories = MenuItem.objects.exclude(option_category__exact='').filter(option=item_id).order_by('option_category').values('option_category').distinct()
	all_categories = []
	for category in all_option_categories:
		current_category = {}
		current_category['name'] = category['option_category']
		all_categories.append(current_category)
	menu_item_options = []
	for option in all_options:
		current_option = {}
		current_option['item_id'] = option.item_id
		current_option['category'] = option.option_category
		current_option['name'] = option.name
		current_option['choose_one'] = option.choose_one
		current_option['removable'] = option.removable
		current_option['price'] = str(option.price)
		menu_item_options.append(current_option)
	response = {'status' : 1, 'all_options' : menu_item_options, 'all_categories' : all_categories}
	return HttpResponse(json.dumps(response), content_type='application/json')