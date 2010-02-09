from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

from agp.views import *

urlpatterns = patterns('',
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),
	(r'^$', include('agp.urls')),
)
