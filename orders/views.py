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
			order_item_detail = Detail(order=current_order, menu_item=menu_item)
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


		send_simple_message(request.POST['emailHTML'])

		cart.clear()


		response = {'status' : 1}


			#show the success page for ordering
		return HttpResponse(json.dumps(response), content_type="application/json")

def success(request):
	if request.method == 'POST':
		current_user = request.user
		restaurant = request.POST['restaurant_id']

	return render(request, 'orders/ordered.html', {})

def send_simple_message(emailHTML):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxc0c1bcb688814d6c94674b7d42ca1018.mailgun.org/messages",
        auth=("api", "key-37d788bd314bf02a7fbb52dfe24efe4a"),
        data={"from": "Excited User <mailgun@sandboxc0c1bcb688814d6c94674b7d42ca1018.mailgun.org>",
              "to": ["manibatra2002@gmail.com"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!",
              "html": "\
  <!DOCTYPE html> <html>\
	<head>\
		<meta charset='utf-8'>\
		<meta http-equiv='X-UA-Compatible' content='IE=edge,chrome=1'>\
		<meta name='viewport' content='width=device-width, minimum-scale=1.0, initial-scale=1, user-scalable=yes'>\
	</head>\
	<body>" +
	emailHTML +
	"</body>\
</html>"})





