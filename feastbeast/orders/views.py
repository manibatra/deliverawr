from django.shortcuts import render
from django.http import HttpResponseRedirect

#importing the auth framework
from django.contrib.auth import authenticate, login

#importing the required models
from users.models import UserAddress
from django.contrib.auth.models import User
from .models import Orders

#importing the cart
from carton.cart import Cart



# Create your views here.

def success(request):

	if request.method == "POST":

		#if its a new shipping address then save it (should there be an option to save it or not?)
		if request.POST['newaddress'] == True:
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

	#creating the Orders objec
	current_order = Orders(user=request.user, restaurant=request.POST['restaurant_id'], total=cart.total)
	current_order.save()
	for product in cart_products:
		current_order.menu_items.add(product.item_id) #maybe can pass it a list of item_ids to fasten up queries

	#clear the cart
	cart.clear()

	#show the success page for ordering
	return render(request, 'orders/ordered.html', {})