from django.conf.urls import patterns, url
from Base import views

urlpatterns = patterns('',
	url(r'^$', views.home, name='home'),
	url(r'^license/view/search/', views.view_licenses_search, name = 'view_licenses_search'),
	url(r'^license/view/page_(?P<pagenum>\S+)/$', views.view_licenses, name = 'view_licenses'),
	url(r'^license/view/(?P<license_id>\d+)/', views.license_detail, name = 'request_detail'),

	url(r'^license/request/$', views.request_form, name = 'request_form'),
	url(r'^license/request/part2/$', views.additional_information, name = 'additional_information'),
	url(r'^license/request_sent/$', views.request_sent, name = 'request_sent'),

	url(r'^license/view_requests/$', views.license_requests, name = 'license_requests'),
	url(r'^license/request/(?P<license_id>\d+)/', views.request_detail, name = 'request_detail'),
	url(r'^license/request/approved/$', views.license_approved, name = 'license_approved'),
	url(r'^license/request/deny_reason/$', views.license_deny_reason, name = 'license_deny_reason'),
	url(r'^license/request/denied/$', views.license_denied, name = 'license_denied'),
	url(r'^license/request/changed/$', views.license_changed, name = 'license_changed'),
		

	url(r'^user/view_requests/$', views.user_requests, name = 'user_requests'),
	url(r'^user/request/approved/$', views.user_approved, name = 'user_approved'),
	url(r'^user/request/denied/$', views.user_denied, name = 'user_denied'), 
	url(r'^user/request/(?P<user_id>\d+)/', views.user_request_detail, name = 'user_request_detail'),

	
	url(r'^password/view_requests/$', views.password_requests, name = 'password_requests'),
	url(r'^password/request/(?P<pass_id>\d+)/', views.password_request_detail, name = 'password_request_detail'),
	url(r'^password/request/approved/$', views.password_request_approve, name = 'password_request_approve'),
	url(r'^password/request/denied/$', views.password_request_deny, name = 'password_request_deny'),
	url(r'^password/change/$', views.change_password, name = 'change_password'),
	url(r'^password/changed/$', views.password_changed, name = 'password_changed'),
)