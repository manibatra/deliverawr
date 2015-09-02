from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.

def landing(request):
	if request.method == "POST":
		first_name = request.POST['firstName']
		last_name = request.POST['lastName']
		email = request.POST['email']
		password = request.POST['password']
		user = User.objects.create_user(email, email, password)
		user.first_name = first_name
		user.last_name = last_name
		user.save()

	context = {}
	return render(request, 'home/index.html', context)

