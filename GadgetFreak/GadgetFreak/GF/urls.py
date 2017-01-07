from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
	url(r'^register/', views.register_user, name='register_user'),
	url(r'^login/', views.login_user, name='login_user'),
	url(r'^logout/', views.logout_user, name='logout'),
    url(r'^$', views.index, name='index')
]
