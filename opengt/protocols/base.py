import logging
logger = logging.getLogger(__name__)

from django_opengt.tracker.models import Tracker, Position


class BaseReport(object):
	IMEI = None
	GPS_fix = None # None, '2D', '3D'
	longitude = None # E1234.1234
	latitude = None # N1234.1234
	altitude = None # altitude in meters
	speed = None # in km/h
	satelites_count = None # Number of satelites in use

	callback = None

	def __init__(self, report_data, callback=None):
		if isinstance(callback, basestring):
			self.callback = __import__(self.callback, globals(), locals(), [''])
		elif callable(callback):
			self.callback = callback
		elif callback:
			logger.warn('Wrong callback type. It must be string or callable object.')

	@property
	def lon(self):
		return self.longitude

	@property
	def lat(self):
		return self.latitude

	@property
	def alt(self):
		return self.altitude

	@property
	def is_valid(self):
		if not self.IMEI:
			logger.warn("Not IMEI")
			return False
		logger.debug('lon: %s, lat: %s' % (self.lon, self.lat))
		if not self.lon or not self.lat:
			logger.debug("no coordinats")
			return False
		return True

	def save(self):
		tracker_qs = Tracker.objects.filter(IMEI=self.IMEI)
		if tracker_qs.count():
			tracker = tracker_qs[0]
		else:
			tracker = None
			logger.warn("Tracker with IMEI %s not found" % self.IMEI)

		p = Position(
						tracker = tracker,
						point = 'POINT(%1.6f %1.6f)' % (self.longitude, self.latitude),
						speed = self.speed,)

		# Run callback
		if callable(self.callback):
			self.callback(p)

		p.save()
		logger.debug("Position with id=%s created" % p.pk)
		return True


import SocketServer
class BaseRequestHandler(SocketServer.BaseRequestHandler):
	report_callback = None
	def setup(self):
		logger.info("%s:%s connected" % self.client_address)

	def finish(self):
		logger.info("%s:%s disconnected" % self.client_address)

