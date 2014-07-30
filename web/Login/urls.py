from django.conf.urls import patterns, url
from Login import views

urlpatterns = patterns('',
	url(r'^$', views.login, name='login_page'),
	url(r'^complete/', views.testo, name='complete'),
	url(r'^new_user/', views.new_user, name='new_user'),
	url(r'^request_sent/', views.request_sent),
	url(r'^logout/$', views.logout),
	url(r'^forgot_password/$', views.forgot_password, name='forgot_password'),
	url(r'^password_request_sent/$', views.password_request_sent, name='password_request_sent'),
)