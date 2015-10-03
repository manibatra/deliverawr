from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^(?P<restaurant_id>[0-9]+)/$', views.detail, name='menu'),
	url(r'^(?P<restaurant_id>[0-9]+)/add/(?P<item_id>[0-9]+)/$', views.add, name='add'),
	url(r'^custom-options/$', views.customOptions, name='custom-options'),
	url(r'^add-custom/$', views.addCustom, name='add-custom'),
	url(r'^get-cart/$', views.getCart, name='get-cart'),
	url(r'^delete-item/$', views.deleteItem, name='delete-item'),
	url(r'^interested/$', views.interested, name='interested'),
]