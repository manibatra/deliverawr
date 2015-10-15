from django.shortcuts import render

def custom_404_view(request):
	return render(request, "custom_error.html", {'heading' : 'HTTP 404 ERROR', 'subheading' : 'Oops! The page you are trying to view does not exist!'})

def custom_500_view(request):
	return render(request, "custom_error.html", {'heading' : 'HTTP 500 ERROR', 'subheading' : 'Oops! Something broke at our end! We are fixing it ASAP!!!'})

def privacy(request):
	return render(request, "company/privacy.html", {})

def disclaimer(request):
	return render(request, "company/disclaimer.html", {})