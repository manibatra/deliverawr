from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^charge/$', views.charge, name='charge'),
	url(r'^add-card/$', views.addCard, name='add_card'),
	url(r'^delete-card/$', views.deleteCard, name='delete_card'),
	url(r'^get-cards/$', views.getCards, name='get_cards'),
	url(r'^make-default/$', views.makeDefault, name='make_default'),
]