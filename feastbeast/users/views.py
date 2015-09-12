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
def get_addresses(requset):
	user_addresses = UserAddress.objects.get(pk=request.user)
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
										phone_no='0414708810')
		user_address.save()

		response = {'status' : 1}

		return HttpResponse(json.dumps(response), content_type='application/json')


	else:
		response = {'status' : 0}

		return HttpResponse(json.dumps(response), content_type='application/json')
