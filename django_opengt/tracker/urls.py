from django.conf.urls.defaults import *
from django_opengt.tracker.views import *

urlpatterns = patterns('',
	url(r'^kml/', kml_trackers),
)
