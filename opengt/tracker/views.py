from tracker.models import Position, Tracker
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def kml_trackers(request):
	trackers = Tracker.objects.filter(view_users=request.user)
	placemarks = ""
	for tr in trackers:
		pos_qs = Position.objects.filter(tracker=tr).order_by('-date')
		if not pos_qs.count():
			continue
		p = pos_qs.order_by('-date')[0].point
		placemarks += """<Placemark><name>1</name><description>Tracker %s</description><angle>0</angle><image>/images/icons/busstop.png</image><graphic>circle</graphic><Point><coordinates>%1.6f, %1.6f</coordinates></Point></Placemark>""" % (tr.pk, p.x, p.y)
	kml = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.2"><Document>%s</Document></kml>""" % placemarks
	return HttpResponse(kml)
