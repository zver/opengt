from protocols.base import BaseReport
from decimaldegrees import dm2decimal

class GlobalsatReport(BaseReport):
	def __init__(self, report_data):
		regex = r'^\$(?P<IMEI>\d+),(?P<status>\d+),(?P<GPS_fix>\d+),(?P<date>\d+),(?P<time>\d+),(?P<longitude>[EW0-9.]+),(?P<latitude>[NS0-9.]+),(?P<altitude>[0-9.]+),(?P<speed>[0-9.]+),(?P<heading>[0-9.]+),(?P<satelites_count>\d+)\*\d+!.*$'
		import re
		m = re.compile(regex).match(str(report_data))
		if not m:
			print "not match!"
			return
		self.IMEI = m.group('IMEI')
		GPS_fix = m.group('GPS_fix')
		if GPS_fix == '1':
			self.GPS_fix = None
		elif GPS_fix == '2':
			self.GPS_fix = '2D'
		elif GPS_fix == '3':
			self.GPS_fix = '3D'
		longitude = m.group('longitude')
		latitude = m.group('latitude')
		longitude = dm2decimal(int(longitude[:4].replace('W', '-').replace('E','')), longitude[4:])
		latitude = dm2decimal(int(latitude[:3].replace('S', '-').replace('N','')), latitude[3])

		self.longitude = longitude
		self.latitude = latitude
		self.altitude = float(m.group('altitude'))
		self.speed = float(m.group('speed')) * 1.852
		self.satelites_count = int(m.group('satelites_count'))


