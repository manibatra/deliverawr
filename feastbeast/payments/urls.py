from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^charge/$', views.charge, name='charge'),
]