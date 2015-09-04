from django.shortcuts import render

# Create your views here.

def detail(request, menu_id):
	context = {'menu_id': menu_id}
	return render(request, 'restaurants/menu.html', context)

