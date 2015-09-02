from django.shortcuts import render

# Create your views here.

def landing(request):
	context = {}
	return render(request, 'home/index.html', context)

