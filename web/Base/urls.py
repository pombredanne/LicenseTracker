from django.conf.urls import patterns, url
from Base import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^view_licenses/search/', views.view_licenses_search, name = 'view_licenses_search'),
	url(r'^view_licenses/page_(?P<pagenum>\S+)/$', views.view_licenses, name = 'view_licenses'),
	url(r'^submit_request/$', views.request_form, name = 'request_form'),
	url(r'^submit_request/additional_information', views.additional_information, name = 'additional_information'),
	url(r'^license_requests/$', views.license_requests, name = 'license_requests'),
	url(r'^request_sent/$', views.request_sent, name = 'request_sent'),
	url(r'^user_requests/$', views.user_requests, name = 'user_requests'),
	url(r'^user_approved/$', views.user_approved, name = 'user_approved'),
	url(r'^user_denied/$', views.user_denied, name = 'user_denied'), 
	url(r'^license_approved/$', views.license_approved, name = 'license_approved'),
	url(r'^license_denied/$', views.license_denied, name = 'license_denied'),
	url(r'^license_changed/$', views.license_changed, name = 'license_changed'),
	url(r'^request/(?P<viewed_username>\w+)/$', views.user_request_detail, name = 'user_request_detail'),
	url(r'^license_request/(?P<license_id>\d+)/', views.request_detail, name = 'request_detail'),
	url(r'^license/(?P<license_id>\d+)/', views.license_detail, name = 'request_detail'),
)