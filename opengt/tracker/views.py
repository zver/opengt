from tracker.models import Positions
def kml_trackers(request):
	p = Position.objects.all().order_by('-date')[0].point
	kml = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.2"><Document><Placemark><name>1</name><description>Маршрут № 1</description><angle>0</angle><image>/images/icons/busstop.png</image><graphic>circle</graphic><Point><coordinates>%1.6f, %1.6f</coordinates></Point></Placemark></Document></kml>""" % (p.x, p.y)
	return HttpResponse(kml)
