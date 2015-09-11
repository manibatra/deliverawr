from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^charge/$', views.charge, name='charge'),
	url(r'^addCard/$', views.add_card, name='add_card'),
]