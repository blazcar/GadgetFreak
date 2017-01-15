from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
	url(r'^register/', views.register_user, name='register_user'),
	url(r'^login/', views.login_user, name='login_user'),
	url(r'^logout/', views.logout_user, name='logout'),
	url(r'^write_article', views.write_article, name='write_article'),
	url(r'^article/(?P<article_id>[0-9]+)/write_comment', views.write_comment, name='write_comment'),
	url(r'^article/(?P<article_id>[0-9]+)/article_delete', views.article_delete, name='article_delete'),
	url(r'^article/(?P<article_id>[0-9]+)/article_view', views.article_view, name='article_view'),
		  url(r'^article/(?P<article_id>[0-9]+)/edit/', views.article_edit, name='article_edit'),
	url(r'^comment/(?P<comment_id>[0-9]+)/$', views.comment_view, name='comment_view'),
  url(r'^comment/(?P<comment_id>[0-9]+)/edit/comment_delete', views.comment_delete, name='comment_delete'),
	url(r'^comment/(?P<comment_id>[0-9]+)/edit/$', views.comment_edit, name='comment_edit'),
	url(r'^$', views.index, name='index'),
]
