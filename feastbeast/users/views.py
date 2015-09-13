from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
import json

#importing the models
from .models import UserAddress


# Create your views here.
def login_user(request):
	email = request.POST['email']
	password = request.POST['password']
	current_page = request.POST['orgpath']
	user = authenticate(username=email, password=password)
	if user is not None:
		if user.is_active:
			login(request, user)
			return HttpResponseRedirect(current_page)
		else:
			return HttpResponse('Invalid User')
	else:
		return HttpResponse('Invalid Credentials')


def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse('home:landing'))

#a function to get all the user addresses
def get_addresses(request):
	user_address_info = UserAddress.objects.filter(user=request.user)
	user_addresses=[]
	for address in user_address_info:
		user_address = {}
		user_address['street_address'] = address.street_address
		user_address['id'] = address.id
		user_address['postcode'] = address.postcode
		user_address['default'] = address.default
		user_addresses.append(user_address)
	response = { 'user_addresses': user_addresses}
	return HttpResponse(json.dumps(response), content_type='application/json')

#function to save the address of the user from the database
def save_address(request):
	if request.method == 'POST':
		current_user = request.user
		street_address = request.POST['street_address']
		postcode = request.POST['postcode']
		country = request.POST['country']
		#TODO : add the city field to the database

		#creating a user address object from the delivery address
		user_address = UserAddress(user=current_user, street_address=street_address, country=country, postcode=postcode,
										phone_no='0414708810',default=True)
		user_address.save()

		response = {'status' : 1}

		return HttpResponse(json.dumps(response), content_type='application/json')


	else:
		response = {'status' : 0}

		return HttpResponse(json.dumps(response), content_type='application/json')

#function to delete a particular address
def delete_address(request):
	if request.method == 'POST':
		address_id = request.POST['address_id']
		user_address = UserAddress.objects.get(pk=address_id)
		user_address.delete()
		try:
			default_address = UserAddress.objects.get(default=True, user=request.user)
			response = {'status': 1}  # the address was deleted
		except UserAddress.DoesNotExist:
			try:
				new_default_address = UserAddress.objects.filter(user=request.user).latest('id')
				new_default_address.default = True
				new_default_address.save()
				response = {'status' : 2, 'default_id' : new_default_address.id} #the address was delted and new default add_id is sent
			except UserAddress.DoesNotExist:
				response = {'status' : 3} #there are no more addresses left
		return HttpResponse(json.dumps(response), content_type='application/json')



#function to set the default address
def setdefault_address(request):
	if request.method == 'POST':
		new_default = UserAddress.objects.get(pk=request.POST['address_id'])
		new_default.default = True
		new_default.save()
		response = {'status' : 1, 'street_address' : new_default.street_address}
	else:
		response = {'status' : 0}

	return HttpResponse(json.dumps(response), content_type='application/json')