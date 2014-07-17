from django.conf.urls import patterns, url
from Login import views

urlpatterns = patterns('',
	url(r'^$', views.login, name='login_page'),
	url(r'^complete/', views.testo),
	url(r'^new_user/', views.new_user),
	url(r'^request_sent/', views.request_sent),
	url(r'^logout/$', views.logout),
)