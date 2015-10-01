from django.conf.urls import url

from . import views

urlpatterns = [
	url((r'^success/$'), views.success, name='success'),
	url((r'^place/$'), views.place, name='place'),
	url((r'^invoice/(?P<order_id>[0-9]+)/$'), views.order_invoice, name='order_invoice'),
]