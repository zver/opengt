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
