import logging
logger = logging.getLogger(__name__)

from django_opengt.tracker.models import Tracker, Position


class BaseReport:
	IMEI = None
	GPS_fix = None # None, '2D', '3D'
	longitude = None # E1234.1234
	latitude = None # N1234.1234
	altitude = None # altitude in meters
	speed = None # in km/h
	satelites_count = None # Number of satelites in use
	
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
		if not tracker_qs.count():
			logger.warn("Tracker with IMEI %s not found" % self.IMEI)
			return False
		tracker = tracker_qs[0]
		p = Position.objects.create(
									tracker = tracker,
									point = 'POINT(%1.6f %1.6f)' % (self.longitude, self.latitude),
									speed = self.speed,)
		logger.debug("Position with id=%s created" % p.pk)
		return True


import SocketServer
class BaseRequestHandler(SocketServer.BaseRequestHandler):
	def setup(self):
		logger.info("%s:%s connected" % self.client_address)
	def finish(self):
		logger.info("%s:%s disconnected" % self.client_address)

