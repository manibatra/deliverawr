from django.shortcuts import render
from django.http import HttpResponse
import json

#importing the auth framework
from django.contrib.auth import authenticate, login

#importing the required models
from users.models import UserAddress
from django.contrib.auth.models import User
from restaurants.models import Restaurant

#importing the cart
from carton.cart import Cart



# Create your views here. 

def place(request):


	response = { 'status' :  1}

	#show the success page for ordering
	return HttpResponse(json.dumps(response), content_type='application/json')

def success(request):
	if request.method == 'POST':
		current_user = request.user
		restaurant = request.POST['restaurant_id']

	return render(request, 'orders/ordered.html', {})