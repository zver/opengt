from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.conf import settings

from pyproj import Geod
import datetime

from django_opengt.tracker.models import Position, Tracker

import logging
logger = logging.getLogger(__name__)

def kml_trackers(request):
	trackers = Tracker.objects.filter(Q(view_users=request.user) | Q(creator=request.user))
	placemarks = ""
	g = Geod(ellps='clrk66')
	added_tracker_pks = []
	for tr in trackers:
		if tr.pk in added_tracker_pks:
			continue
		added_tracker_pks.append(tr.pk)
		pos_qs = Position.objects.filter(tracker=tr).order_by('-date')
		count = pos_qs.count()
		if not count:
			continue
		pos_qs = pos_qs.order_by('-date')
		pos = pos_qs[0]
		p = pos.point
		p_prev = None
		angle = 0.0
		stay = None
		if datetime.datetime.now() - pos.date > datetime.timedelta(seconds=settings.MIN_LINK_TIMEOUT):
			stay = True
		elif pos.speed != None:
			stay = pos.speed <= settings.STAY_AVG_SPEED
		if count > 1:
			pos_prev = pos_qs[1]
			p_prev = pos_prev.point
			angle, angle2, dist = g.inv(p_prev.x, p_prev.y, p.x, p.y)
			if stay == None:
				avg_speed = dist/float((pos.date-pos_prev.date).seconds)
				avg_speed = avg_speed*10/36.
				logger.debug("avg_speed: %s" % avg_speed)
				stay = avg_speed <= settings.STAY_AVG_SPEED
		if stay == None:
			stay = True
		if stay:
			image_url = settings.MEDIA_URL + 'images/icons/busstop.png'
			graphic = 'circle'
			angle = 0.0
		else:
			image_url = settings.MEDIA_URL + 'images/icons/bus.png'
			graphic = 'bus'

		marker_color = tr.marker_color if tr.marker_color else '00ff00'
		placemarks += """<Placemark><name>%s</name><description>%s</description><angle>%1.4f</angle><image>%s</image><graphic>%s</graphic><marker_color>#%s</marker_color><Point><coordinates>%1.6f,%1.6f</coordinates></Point></Placemark>""" % (tr.name, tr.description, angle, image_url, graphic, marker_color, p.x, p.y)
	kml = """<?xml version="1.0" encoding="UTF-8"?><kml xmlns="http://earth.google.com/kml/2.2"><Document>%s</Document></kml>""" % placemarks
	return HttpResponse(kml)

def gpx_trackers(request, last_seconds):
	""" Return GPX file format for all view trackers with limit by last_seconds """
	trackers = Tracker.objects.filter(Q(view_users=request.user) | Q(creator=request.user))
	gpx = '''<?xml version="1.0"?><gpx version="1.0" creator="Django opengt" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://www.topografix.com/GPX/1/0" xsi:schemaLocation="http://www.topografix.com/GPX/1/0 http://www.topografix.com/GPX/1/0/gpx.xsd">'''
	from django_opengt.tracker.utils import get_segments
	min_date = datetime.datetime.now() - datetime.timedelta(seconds=int(last_seconds))
	for tr in trackers:
		segments = get_segments(tr.positions.filter(date__gte=min_date).order_by('date'))
		if not segments:
			continue
		gpx += '<trk>\n<name>%s</name>\n' % tr.name
		for seg in segments:
			gpx += '<trkseg>\n'
			for pos in seg:
				gpx += '<trkpt lat="%(lat)1.6f" lon="%(lon)1.6f"><time>%(time)s</time></trkpt>\n' % {
						'lat'		: pos.point.y,
						'lon'		: pos.point.x,
						'time'		: pos.date.isoformat(),
				}
			gpx += '</trkseg>\n'
		gpx += '</trk>\n'
	gpx += '</gpx>\n'

	return HttpResponse(gpx)
