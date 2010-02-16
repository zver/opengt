from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.conf import settings

from pyproj import Geod

from tracker.models import Position, Tracker

def kml_trackers(request):
	trackers = Tracker.objects.filter(Q(view_users=request.user) | Q(creator=request.user))
	placemarks = ""
	g = Geod(ellps='clrk66')
	for tr in trackers:
		pos_qs = Position.objects.filter(tracker=tr).order_by('-date')
		count = pos_qs.count()
		if not count:
			continue
		pos_qs = pos_qs.order_by('-date')
		pos = pos_qs[0]
		p = pos.point
		p_prev = None
		angle = 0.0
		stay = True
		if count > 1:
			p_prev = pos_qs[1].point
			angle, angle2, dist = g.inv(p_prev.x, p_prev.y, p.x, p.y)
			if dist < settings.MIN_STAY_DISTANCE \
				or pos.speed == 0 \
				or datetime.datetime.now() - pos.date > datetime.timedelta(seconds=settings.MIN_LINK_TIMEOUT):
				stay = True
			else:
				stay = False

		if stay:
			image_url = settings.MEDIA_URL + 'images/icons/bus.png'
			graphic = 'bus'
			angle = 0.0
		else:
			image_url = settings.MEDIA_URL + 'images/icons/busstop.png'
			graphic = 'circle'

		placemarks += """<Placemark><name>%s</name><description>%s</description><angle>%1.4f</angle><image>%s</image><graphic>%s</graphic><Point><coordinates>%1.6f,%1.6f</coordinates></Point></Placemark>""" % (tr.name, tr.description, angle, image_url, graphic, p.x, p.y)
	kml = """<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://earth.google.com/kml/2.2"><Document>%s</Document></kml>""" % placemarks
	return HttpResponse(kml)
