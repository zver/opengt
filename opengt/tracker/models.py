from django.contrib.gis.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

PROTOCOLS = (
		('globalsat', 'Globalsat'),
)

class Model(models.Model):
	name = models.CharField(_('Name'), max_length=60, help_text=_('Example: TR-102'))
	protocol = models.SlugField(_('Protocol'), choices=PROTOCOLS)
	class Meta:
		verbose_name = _('Tracker model')
		verbose_name_plural = _('Tracker models')
	def __unicode__(self):
		return u'%s (%s)' % (self.name, self.protocol)

class Type(models.Model):
	name = models.CharField(_('Name'), max_length=60, help_text=_('Example: car, velo'))
	class Meta:
		verbose_name = _('Tracker type')
		verbose_name_plural = _('Tracker types')
	def __unicode__(self):
		return self.name

class Tracker(models.Model):
	IMEI = models.CharField(u'IMEI', max_length=60, unique=True)
	name = models.CharField(_('Name'), max_length=60)
	description = models.TextField(_('Description'), blank=True, null=True)
	model = models.ForeignKey(Model, verbose_name=_('Model'))
	type = models.ForeignKey(Type, verbose_name=_('Type'), blank=True, null=True)
	creator = models.ForeignKey(User, verbose_name=_('Creator'), related_name='trackers_by_creator')
	view_users = models.ManyToManyField(User, verbose_name=_('View users'), related_name='trackers_by_viewer', blank=True, null=True)
	view_groups = models.ManyToManyField(Group, verbose_name=_('View groups'), blank=True, null=True)

	class Meta:
		verbose_name = _('Tracker')
		verbose_name_plural = _('Trackers')
	def __unicode__(self):
		return u'%s (IMEI: %s, %s)' % (self.model, self.IMEI, self.type)
	def get_stats(self, start_date=None, end_date=None):
		link_time = 0
		move_time = 0
		stay_time = 0
		distance = 0

		qs = self.positions.all()
		if start_date:
			qs = qs.filter(date__gte=start_date)
		if end_date:
			qs = qs.filter(date__lte=end_date)

		prev_p = None
		from pyproj import Geod
		g = Geod(ellps='clrk66')
		for p in qs:
			if not prev_p or (p.date-prev_p.date).seconds == 0:
				prev_p = p
				continue
			time_delta = (p.date-prev_p.date).seconds
			if time_delta < settings.MIN_LINK_TIMEOUT:
				link_time += time_delta
				angle, angle2, dist = g.inv(prev_p.point.x, prev_p.point.y, p.point.x, p.point.y)
				s = (p.date-prev_p.date).seconds
				avg_speed = float(dist)/float((p.date-prev_p.date).seconds)
				avg_speed = avg_speed*10.0/36.
				if avg_speed > settings.STAY_AVG_SPEED:
					stay_time += time_delta
				distance += dist

			move_time = link_time - stay_time

			prev_p = p
		return 	{	
					'link_time'	: link_time,
					'move_time'	: move_time,
					'stay_time' : stay_time,
					'distance'	: distance,
				}

	_stats = {}
	@property
	def stats(self):
		if not self._stats:
			self._stats = self.get_stats()
		return self._stats


class Position(models.Model):
	date = models.DateTimeField(_('Date'), auto_now_add=True)
	tracker = models.ForeignKey(Tracker, verbose_name=_('Tracker'), related_name='positions')
	point = models.PointField(_('Point'))
	speed = models.FloatField(_('Speed'), help_text=_('Speed in km/h'), blank=True, null=True)
	objects = models.GeoManager()
	def __unicode__(self):
		return u'%s %s' % (self.date, self.tracker)
	class Meta:
		verbose_name = _('Position')
		verbose_name_plural = _('Positions')

