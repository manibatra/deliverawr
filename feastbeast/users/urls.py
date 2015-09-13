from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^login/$', views.login_user, name='login_user'),
	url(r'^logout/$', views.logout_user, name='logout_user'),
	url(r'^save_address/$', views.save_address, name='save_address'),
	url(r'^delete_address/$', views.delete_address, name='delete_address'),
	url(r'^get_addresses/$', views.get_addresses, name='get_addresses'),
	url(r'^setdefault_address/$', views.setdefault_address, name='setdefault_address'),
]