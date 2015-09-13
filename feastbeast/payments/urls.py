from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^charge/$', views.charge, name='charge'),
	url(r'^add_card/$', views.add_card, name='add_card'),
	url(r'^get-cards/$', views.getCards, name='get_cards'),
]