from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
import json
from django.conf import settings
import os


#importing the auth framework
from django.contrib.auth import authenticate, login

#importing the required models
from users.models import UserAddress, UserPhoneNo
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
		phoneNo_object = UserPhoneNo.objects.get(user=current_user)
		restaurant_id = request.POST['restaurant_id']
		delivery_address = UserAddress.objects.get(user=current_user, default=True)

		restaurant = Restaurant.objects.get(pk=restaurant_id)
		current_order = UserOrder(user=current_user, restaurant=restaurant, total_price=float(cart.total), delivery_address=delivery_address,
									phone_no=phoneNo_object)
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

		#getting the template
		template = loader.get_template("billing.html")

		#creating the context
		order_dict = generate_order_dict(current_order)


		#creating the context
		context = Context(order_dict)


		#rendering the template
		emailHTML = template.render(context)


		send_simple_message(current_user.email, emailHTML)

		send_sms_customer(request.META['HTTP_HOST'], current_order.order_id, phoneNo_object.phone_no)

		cart.clear()


		response = {'status' : 1}


		#show the success page for ordering
		return HttpResponse(json.dumps(response), content_type="application/json")

	else:
		raise Http404()



#function to show the order on page
def order_invoice(request, order_id):
	try:
		current_order =  UserOrder.objects.get(order_id=order_id)
		if current_order.user.id == request.user.id:
			context_dict = generate_order_dict(current_order)
			return render(request, "orders/order_invoice.html", context_dict)
	except:
		raise Http404()

	else:
	    raise Http404()


#function takes the current delivery object, and creates a context out of it
def generate_order_dict(current_order):

	order_dict = {}
	#adding user name to context
	order_dict['user'] = current_order.user.first_name + " " + current_order.user.last_name

	#adding the restaurant name
	order_dict['restaurant'] = current_order.restaurant.name

	#adding user address to context
	order_dict['street_address'] = current_order.delivery_address.street_address
	order_dict['city'] = current_order.delivery_address.city
	order_dict['postcode'] = current_order.delivery_address.postcode

	#adding the order to the context
	items = Detail.objects.filter(order=current_order)
	order_dict['items'] = items

	#adding the total price to the context
	order_dict['total'] = current_order.total_price


	return order_dict

#shows the succes page after succesful placement of order
def success(request):
	return render(request, 'orders/ordered.html', {})

#method to send the mail to the customer
def send_simple_message(customer_email, emailHTML):
    return requests.post(
        settings.MAILGUN_URL + "/messages",
        auth=("api", settings.MAILGUN_API_KEY),
        data={"from": "Deliverawr <mailgun@" + settings.MAILGUN_DOMAIN + ">",
              "to": [customer_email, 'manibatra2002@gmail.com'],
              "subject": "Thank you for ordering",
              "html": emailHTML
	})


def send_sms_customer(domain, order_id, customer_phoneNo):
	URL = "https://api.smsbroadcast.com.au/api.php"
	payload = {
    'username': settings.SMS_USERNAME,
    'password': settings.SMS_PASSWORD,
    'from': 'Deliverawr',
    'to' : customer_phoneNo,
    'message' : 'Thank you for ordering. We are on our way. Check your invoice : '+ domain + '/orders/invoice/' + str(order_id)
	}

	r = requests.post(URL, data=payload)




