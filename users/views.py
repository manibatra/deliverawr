from django.shortcuts import render
from django.conf import settings

#auth related imports
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

#imports for validation
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from django.http import HttpResponseRedirect,HttpResponse, Http404
from django.core.urlresolvers import reverse
import json
from .utils import *

#importing the models
from .models import UserAddress
from .models import UserPhoneNo, UserVerification
from django.utils.crypto import get_random_string





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

			#checking validity of phoneNo
			phoneNo = request.POST['phoneNo']
			if len(phoneNo) != 10:
				raise ValidationError("PhoneNo length should be 10")

		    #checking min pasword length
			password = request.POST['password']
			if len(password) < 6:
				raise ValidationError("Minimum password length should be 6")

		except (KeyError, ValidationError) as e:
			response = {'status' : 0, 'msg' : str(e)}
			return HttpResponse(json.dumps(response), content_type='application/json')

		response = {}

		try:
			user = User.objects.create_user(email, email, password)
			user.first_name = first_name
			user.last_name = last_name
			user.is_active = False
			user.save()

			user_phoneNo = UserPhoneNo(user=user, phone_no=phoneNo)
			user_phoneNo.save()
			response = {'status' : 1}

			ver_key = get_random_string(32)
			user_ver_object = UserVerification(user=user, ver_code=ver_key)
			user_ver_object.save()
			user_uuid = user_ver_object.id

			ver_key_url = request.build_absolute_uri("/user/verification-confirm/")
			ver_key_url = ver_key_url + str(user_uuid) + ver_key

			emailHTML = generate_email_HTML(ver_key_url)

			send_confirmation_email(user.email, emailHTML)

		except IntegrityError:
			response = {'status' : 0, 'msg' : 'User with the entered email already exists'}
			return HttpResponse(json.dumps(response), content_type='application/json')

		except:
			response = {'status' : 0, 'msg' : 'Things just blew up. Contact us at manibatra2002@gmail.com'}
			return HttpResponse(json.dumps(response), content_type='application/json')

		# user = authenticate(username=email, password=password)
		# if user is not None:
		# 	if user.is_active:
		# 		login(request, user)
		# 		response = {'status' : 1}

		# 	else:
		# 		response = {'status' : 0, 'msg' : 'user could not be loged in! try again'}
		# else:
		# 	response = {'status' : 0, 'msg' : 'user could not be loged in! try again'}
	else:
		raise Http404()

	return HttpResponse(json.dumps(response), content_type='application/json')


#method to show a view indacting user to confirm
def verification_start(request):
	context = { 'text' : 'A confirmation email has been sent to your email address. Click on the confirmation\
					link in your email to activate your account', 'heading' : 'confirm your email address' }
	return render(request, 'users/verification.html', context)

#view to show when user clicks the confirmation link
def verification_confirm(request, uuid, ver_code):
	user_ver_object = UserVerification.objects.get(id=uuid)
	if ver_code == user_ver_object.ver_code:
		user = user_ver_object.user
		user.is_active = True
		user.save()
		return HttpResponseRedirect(reverse("users:verification_complete"))

	else:
		context = { 'text' : 'You have arrived here via an invalid link\
					', 'heading' : 'Invalid Link' }
	return render(request, 'users/verification.html', context)

#method to complete the verification process
def verification_complete(request):
	context = { 'text' : 'Your email has been confirmed. You can login and start using Delivrawr now.\
					', 'heading' : 'Email Address Confirmed' }
	return render(request, 'users/verification.html', context)

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
				response = {'status' : 0, 'msg' : 'Please confirm your email address to login'}
		else:
			response = {'status' : 0, 'msg' : 'user could not be loged in! try again'}

	else:
		raise Http404()

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
			country = 'Australia'
			city = request.POST['city']
			#TODO : add the city field to the database

			#creating a user address object from the delivery address
			user_address = UserAddress(user=current_user, street_address=street_address,city=city , country=country, postcode=postcode,
											default=True)
			user_address.save()

			response = {'status' : 1}

			return HttpResponse(json.dumps(response), content_type='application/json')
		else:
			return HttpResponse("Invalid request - 404")


	else:
		raise Http404()

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
	else:
		raise Http404()



#function to set the default address
def setdefault_address(request):
	if request.method == 'POST':
		new_default = UserAddress.objects.get(pk=request.POST['address_id'])
		new_default.default = True
		new_default.save()
		response = {'status' : 1, 'street_address' : new_default.street_address}
	else:
		raise Http404()
	return HttpResponse(json.dumps(response), content_type='application/json')

#render the expression of interest view
def interested(request):
	return render(request, "users/driver_interest.html", {'heading' : 'Apply as a Driver', 'subheading' : 'Earn atleast $20 per hour',
															 'show_form' : True})

#render the expression of interest view
def notify_deliverawr(request):
	if request.method == 'POST':
		driver_name = request.POST['Name']
		email_id = request.POST['email']
		phoneNo = request.POST['phoneNo']
		suburb = request.POST['city']
		text_to_send = driver_name + ':' + email_id + ':' + phoneNo + suburb
		send_mail_deliverawr(text_to_send)
		return render(request, "users/driver_interest.html", {'heading' : 'Thank You', 'subheading' : 'Our team will be contacting you to\
																schedule an interview ASAP', 'show_form' : False})
	else:
		raise Http404()