"""feastbeast URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
	url(r'^', include('home.urls', namespace="home")),
	url(r'^restaurant/', include('restaurants.urls', namespace="restaurants")),
    url(r'^{}/admin/'.format(settings.ADMIN_URL_PATH), include(admin.site.urls)),
    url(r'^payments/', include('payments.urls', namespace="payments")),
    url(r'^user/', include('users.urls', namespace="users")),
    url(r'^orders/', include('orders.urls', namespace="orders")),
    url(r'^password/reset-password/$', auth_views.password_reset, {'template_name': 'password.html'}, name='password_reset'),
    url(r'^password/reset-password-done/$', auth_views.password_reset_done, {'template_name': 'password_reset_done.html'}, name="password_reset_done"),
    url(r'^password/reset-password-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm, {'template_name': 'password_reset_confirm.html'}, name="password_reset_confirm"),
    url(r'^password/reset-password-complete/$', auth_views.password_reset_complete, {'template_name': 'password_reset_complete.html'}, name="password_reset_complete"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )