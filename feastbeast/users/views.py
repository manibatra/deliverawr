from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect


# Create your views here.
def login(request):
	def my_view(request):
		email = request.POST['email']
		password = request.POST['password']
		current_page = request.POST['origpath']
		user = authenticate(username=email, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect(current_page)
			else:
				pass
		else:
			pass
