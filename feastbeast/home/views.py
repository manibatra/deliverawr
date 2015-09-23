from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from restaurants.models import Restaurant


# Create your views here.

def landing(request):

	context = {}
	return render(request, 'home/index.html', context)

def listings(request):
	postcode = request.GET['postcode']
	restaurant_list = Restaurant.objects.filter(deliverylocation__postcode=str(postcode))
	if len(restaurant_list) > 0:
		restaurant_found = 'yes'
		context = { 'restaurant_found' : restaurant_found, 'restaurant_list' : restaurant_list}
	else:
		restaurant_found = 'no'
		context = { 'restaurant_found' : restaurant_found}

	return render(request, 'home/listings.html', context)





