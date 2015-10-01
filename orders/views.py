from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
import json

#importing the auth framework
from django.contrib.auth import authenticate, login

#importing the required models
from users.models import UserAddress
from django.contrib.auth.models import User
from restaurants.models import Restaurant, MenuItem
from .models import UserOrder, Detail

#importing the cart
from restaurants.mycart import ModifiedCart

#importing requests lib to send mail
import requests

#importing the django templete renderer
from django.template import loader, Context



# Create your views here.

def place(request):

	if request.method == 'POST':
		cart = ModifiedCart(request.session)
		current_user = request.user

		restaurant_id = request.POST['restaurant_id']
		delivery_address = UserAddress.objects.get(user=current_user, default=True)

		restaurant = Restaurant.objects.get(pk=restaurant_id)
		current_order = UserOrder(user=current_user, restaurant=restaurant, total_price=float(cart.total), delivery_address=delivery_address)
		current_order.save()
		serialised_cart = cart.cart_serializable
		item_keys = serialised_cart.keys()
		for key in item_keys:
			item_object = serialised_cart[key]
			menu_item = MenuItem.objects.get(pk=item_object['product_pk'])

			#creating the detail object for the particular menu item
			order_item_detail = Detail(order=current_order, menu_item=menu_item,subtotal=float(item_object['subtotal']))
			order_item_detail.save()


			#get the add ons and items removed
			add_ons_list = json.loads(item_object['add_ons'])
			removed_list = json.loads(item_object['removed'])

			all_add_ons = []
			all_removed = []


			if len(add_ons_list) > 0: #iterate trhought the list of addons
				for add_item in add_ons_list:
					add_on_product = MenuItem.objects.get(pk=add_item['product_pk'])
					all_add_ons.append(add_on_product)

			if len(removed_list) > 0: #iterate trhought the list of removed items
				for remove_item in removed_list:
					remove_product = MenuItem.objects.get(pk=remove_item['product_pk'])
					all_removed.append(remove_product)

			order_item_detail.add_ons.add(*all_add_ons)
			order_item_detail.removed.add(*all_removed)

		# #adding user name to context
		# email_context['user'] = request.user.first_name + " " + request.user.last_name

		# #adding user address to context
		# email_context['street_address'] = delivery_address.street_address
		# email_context['postcode'] = delivery_address.postcode

		# #adding the order to the context
		# items = Detail.objects.filter(order=current_order)
		# email_context['items'] = items

		# #adding the total price to the context
		# email_context['total'] = cart.total

		#getting the template
		template = loader.get_template("billing.html")

		#creating the context
		context = generate_order_request(current_order)

		#rendering the template
		emailHTML = template.render(context)


		send_simple_message(emailHTML)

		cart.clear()


		response = {'status' : 1}


		#show the success page for ordering
		return HttpResponse(json.dumps(response), content_type="application/json")

#function takes the current delivery object, and creates a context out of it
def generate_order_request(current_order):

	email_context = {}
	#adding user name to context
	email_context['user'] = current_order.user.first_name + " " + current_order.user.first_name

	#adding the restaurant name
	email_context['restaurant'] = current_order.restaurant.name

	#adding user address to context
	email_context['street_address'] = current_order.delivery_address.street_address
	email_context['postcode'] = current_order.delivery_address.postcode

	#adding the order to the context
	items = Detail.objects.filter(order=current_order)
	email_context['items'] = items

	#adding the total price to the context
	email_context['total'] = current_order.total_price

	#creating the context
	context = Context(email_context)

	return context

#shows the succes page after succesful placement of order
def success(request):
	if request.method == 'POST':
		current_user = request.user
		restaurant = request.POST['restaurant_id']

	return render(request, 'orders/ordered.html', {})

#method to send the mail to the customer
def send_simple_message(emailHTML):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxc0c1bcb688814d6c94674b7d42ca1018.mailgun.org/messages",
        auth=("api", "key-37d788bd314bf02a7fbb52dfe24efe4a"),
        data={"from": "Excited User <mailgun@sandboxc0c1bcb688814d6c94674b7d42ca1018.mailgun.org>",
              "to": ["manibatra2002@gmail.com"],
              "subject": "Thank you for ordering",
              "html": emailHTML
	})





