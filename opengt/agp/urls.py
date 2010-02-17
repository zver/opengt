from django.conf.urls.defaults import *
from agp.views import *



urlpatterns = patterns('',
	url(r'^$', index, name="index"),
	url(r'^map/$', map, name="map"),
	url(r'^login/$', login, name="login"),
	url(r'^logout/$', logout, name="logout"),
	url(r'^registration/$', registration, name="registration"),
	url(r'^trackers/$', trackers, name="trackers"),
	url(r'^trackers/(?P<tracker_id>\d+)/$', edit_tracker, name="edit_tracker"),
	url(r'^trackers/del/(?P<tracker_id>\d+)/$', del_tracker, name="del_tracker"),

)
