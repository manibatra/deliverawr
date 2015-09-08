from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse


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
