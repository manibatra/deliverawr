from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from restaurants.models import Restaurant


# Create your views here.

def success(request):

	if request.method == "POST":
		first_name = request.POST['firstName']
		last_name = request.POST['lastName']
		email = request.POST['email']
		password = request.POST['password']
		user = User.objects.create_user(email, email, password)
		user.first_name = first_name
		user.last_name = last_name
		user.save()
		user = authenticate(username=email, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('')


	context = {}
	return render(request, 'orders/ordered.html', context)