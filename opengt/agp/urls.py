from django.conf.urls.defaults import *
from agp.views import *



urlpatterns = patterns('',
	url(r'^$', index, name="index"),
	url(r'^map/$', map, name="map"),
	url(r'^login/$', login, name="login"),
	url(r'^registration/$', registration, name="registration"),
)
