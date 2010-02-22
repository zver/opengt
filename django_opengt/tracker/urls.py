from django.conf.urls.defaults import *
from tracker.views import *

urlpatterns = patterns('',
	url(r'^kml/', kml_trackers),
)
