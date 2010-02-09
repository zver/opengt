from django.conf.urls.defaults import *
from agp.views import *



urlpatterns = patterns('',
	url(r'^$', index, name="index"),
	url(r'^map/$', map, name="map"),
)
