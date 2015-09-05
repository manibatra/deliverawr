from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^(?P<restaurant_id>[0-9]+)/$', views.detail, name='menu'),
	url(r'^(?P<restaurant_id>[0-9]+)/add/(?P<item_id>[0-9]+)/$', views.add, name='add'),
]