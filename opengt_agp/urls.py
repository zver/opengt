from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from agp.views import *

urlpatterns = patterns('',
	(r'^admin/doc/', include('django.contrib.admindocs.urls')),
	(r'^admin/', include(admin.site.urls)),
	(r'^', include('agp.urls')),
	(r'^trackers/', include('django_opengt.tracker.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'm/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
	)


urlpatterns += patterns('',
	url(r'^', include('cms.urls')),
)
