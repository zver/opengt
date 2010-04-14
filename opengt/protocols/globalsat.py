from opengt.protocols.base import BaseReport
from decimaldegrees import dm2decimal

import logging
logger = logging.getLogger(__name__)

class GlobalsatReport(BaseReport):
	def __init__(self, report_data, callback=None):
		super(GlobalsatReport, self).__init__(report_data, callback=None)
		regex = r'^\$(?P<IMEI>\d+),(?P<status>\d+),(?P<GPS_fix>\d+),(?P<date>\d+),(?P<time>\d+),(?P<longitude>[EW0-9.]+),(?P<latitude>[NS0-9.]+),(?P<altitude>-?[0-9.]+),(?P<speed>[0-9.]+),(?P<heading>[0-9.]+),(?P<satelites_count>\d+)\*\d+!.*$'
		import re
		m = re.compile(regex).match(str(report_data))
		if not m:
			logger.info("data doesn't match.")
			return
		self.IMEI = m.group('IMEI')
		GPS_fix = m.group('GPS_fix')
		if GPS_fix == '1':
			self.GPS_fix = None
		elif GPS_fix == '2':
			self.GPS_fix = '2D'
		elif GPS_fix == '3':
			self.GPS_fix = '3D'

		if self.GPS_fix:
			longitude = m.group('longitude')
			latitude = m.group('latitude')
			longitude = dm2decimal(int(longitude[:4].replace('W', '-').replace('E','')), longitude[4:])
			latitude = dm2decimal(int(latitude[:3].replace('S', '-').replace('N','')), latitude[3:])

			self.longitude = longitude
			self.latitude = latitude
			self.altitude = float(m.group('altitude'))
			self.speed = float(m.group('speed')) * 1.852
		self.satelites_count = int(m.group('satelites_count'))


from base import BaseRequestHandler
class GlobalsatRequestHandler(BaseRequestHandler):
	lock = None

	def handle(self):
		while 1:
			data = self.request.recv(1024)

			try:
				logger.debug(u'data: %s' % str(data))
			except:
				logger.debug(u'not printable data')

			if not data: break
			gr = GlobalsatReport(str(data), callback=self.report_callback)
			if gr.is_valid:
				if self.lock:
					with self.lock: gr.save()
				else: gr.save()

