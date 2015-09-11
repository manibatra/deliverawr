from django.shortcuts import render
from django.http import HttpResponse
import json

#importing the auth framework
from django.contrib.auth import authenticate, login

#importing the required models
from users.models import UserAddress
from django.contrib.auth.models import User
from .models import Orders
from restaurants.models import Restaurant

#importing the cart
from carton.cart import Cart



# Create your views here.

def place(request):

	if request.method == "POST":

		#if its a new shipping address then save it (should there be an option to save it or not?)
		new_address = request.POST['new_address']
		if new_address == 'true':
			current_user = request.user
			street_address = request.POST['street_address']
			postcode = request.POST['postcode']
			country = request.POST['country']

			#creating a user address object from the shipping info
			user_address = UserAddress(user=current_user, street_address=street_address, country=country, postcode=postcode,
											phone_no='0414708810')
			user_address.save()


		#get the order info from the cart

		cart = Cart(request.session)
		cart_products = cart.products

		#creating the Orders object
		restaurant_id = request.POST['restaurant_id']
		restaurant = Restaurant.objects.get(pk=restaurant_id)
		current_order = Orders(user=request.user, restaurant=restaurant, total=cart.total)
		current_order.save()
		for product in cart_products:
			current_order.menu_items.add(product.item_id) #maybe can pass it a list of item_ids to fasten up queries

		#clear the cart
		cart.clear()

		response = { 'status' :  1}

	#show the success page for ordering
	return HttpResponse(json.dumps(response), content_type='application/json')

def success(request):
	return render(request, 'orders/ordered.html', {})