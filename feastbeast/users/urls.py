from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^login/$', views.login_user, name='login_user'),
	url(r'^logout/$', views.logout_user, name='logout_user'),
	url(r'^save_address/$', views.save_address, name='save_address'),
]