from django.shortcuts import render

#auth related imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

#imports for validation
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
import json

#importing the models
from .models import UserAddress





# Create your views here.
#method to signup the user and login at the same time
def signupUser(request):
	if request.method == "POST":
		try: #checking the validity of first / last name
			first_name = request.POST['firstName']
			last_name = request.POST['lastName']
			if len(first_name) > 30 or len(first_name) < 2:
				raise ValidationError("Invalid length of first name")

			if len(last_name) > 30 or len(last_name) < 2:
				raise ValidationError("Invalid length of last name")

		    #checking the validity of email
			email = request.POST['email']
			validate_email(email)

		    #checking min pasword length
			password = request.POST['password']
			if len(password) < 6:
				raise ValidationError("Minimum password length should be 6")

		except (KeyError, ValidationError) as e:
			response = {'status' : 0, 'msg' : str(e)}
			return HttpResponse(json.dumps(response), content_type='application/json')

		user = User.objects.create_user(email, email, password)
		user.first_name = first_name
		user.last_name = last_name
		user.save()
		response = {}
		user = authenticate(username=email, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				response = {'status' : 1}

			else:
				response = {'status' : 0, 'msg' : 'user could not be loged in! try again'}
		else:
			response = {'status' : 0, 'msg' : 'user could not be loged in! try again'}
	else:
		response = {'status' : 0, 'msg' : 'invalid request'}

	return HttpResponse(json.dumps(response), content_type='application/json')

#method to login the user
def loginUser(request):
	if request.method == "POST":
		try: #checking the validity of email
			email = request.POST['emailLogIn']
			validate_email(email)

		 	#checking the validity of password
			password = request.POST['passwordLogIn']
			if len(password) < 6:
				raise ValidationError("Minimum password length should be 6")

		except (KeyError, ValidationError) as e:
			response = {'status' : 0, 'msg' : str(e)}
			return HttpResponse(json.dumps(response), content_type='application/json')

		user = authenticate(username=email, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				response = {'status' : 1}
			else:
				response = {'status' : 0, 'msg' : 'user could not be loged in! try again'}
		else:
			response = {'status' : 0, 'msg' : 'user could not be loged in! try again'}

	else:
		response = {'status' : 0, 'msg' : 'invalid request'}

	return HttpResponse(json.dumps(response), content_type='application/json')


def logout_user(request):
	logout(request)
	return HttpResponseRedirect(reverse('home:landing'))

#a function to get all the user addresses
def get_addresses(request):

	if request.user.is_authenticated():
		user_address_info = UserAddress.objects.filter(user=request.user)
	else:
		return HttpResponse("Invalid request - 404")

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

		if request.user.is_authenticated():
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
			return HttpResponse("Invalid request - 404")


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