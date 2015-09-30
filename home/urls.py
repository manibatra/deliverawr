from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^$', views.landing, name='landing'),
	url(r'^listings/$', views.listings, name='listings'),
]