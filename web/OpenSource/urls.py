from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	# Examples:
	# url(r'^$', 'OpenSource.views.home', name='home'),
	# url(r'^blog/', include('blog.urls')),
	
	url(r'^login/', include('Login.urls')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^', include('Base.urls')),

)
