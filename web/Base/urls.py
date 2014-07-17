from django.conf.urls import patterns, url
from Base import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^view_licenses/$', views.view_licenses, name = 'view_licenses'),
	url(r'^submit_request/$', views.request_form, name = 'request_form'),
	url(r'^request_logic/$', views.intermediate_logic, name = 'intermediate_logic'),
	url(r'^submit_request/(?P<license_name>\w+)_version_(?P<license_version>\S+)/$', views.additional_information, name = 'additional_information'),
	url(r'^request_sent/$', views.request_sent, name = 'request_sent'),
	url(r'^user_requests/$', views.user_requests, name = 'user_requests'),
	url(r'^user_approved/$', views.user_approved, name = 'user_approved'),
	url(r'^user_denied/$', views.user_denied, name = 'user_denied'), 
	url(r'^request/(?P<viewed_username>\w+)/$', views.user_request_detail, name = 'user_request_detail'),
	url(r'^license/(?P<license_name>\w+)_version_(?P<license_version>\w+)/$', views.license_detail, name = 'license_detail'),
)