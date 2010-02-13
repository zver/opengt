from django.contrib.gis.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _

PROTOCOLS = (
		('globalsat', 'Globalsaet'),
)

class Model(models.Model):
	name = models.CharField(_('Name'), max_length=60, help_text=_('Example: TR-102'))
	protocol = models.SlugField(_('Protocol'), choices=PROTOCOLS)
	class Meta:
		verbose_name = _('Tracker model')
		verbose_name_plural = _('Tracker models')

class Type(models.Model):
	name = models.CharField(_('Name'), max_length=60, help_text=_('Example: car, velo'))
	class Meta:
		verbose_name = _('Tracker type')
		verbose_name_plural = _('Tracker types')

class Tracker(models.Model):
	IMEI = models.CharField(u'IMEI', max_length=60)
	model = models.ForeignKey(Model, verbose_name=_('Model'))
	type = models.ForeignKey(Type, verbose_name=_('Type'))
	creator = models.ForeignKey(User, verbose_name=_('Creator'), related_name='trackers_by_creator')
	view_users = models.ManyToManyField(User, verbose_name=_('View users'), related_name='trackers_by_viewer', blank=True, null=True)
	view_groups = models.ManyToManyField(Group, verbose_name=_('View groups'), blank=True, null=True)
	class Meta:
		verbose_name = _('Tracker')
		verbose_name_plural = _('Trackers')

class Position(models.Model):
	date = models.DateTimeField(_('Date'), auto_now_add=True)
	tracker = models.ForeignKey(Tracker, verbose_name=_('Tracker'))
	point = models.PointField(_('Point'))
	objects = models.GeoManager()
	class Meta:
		verbose_name = _('Position')
		verbose_name_plural = _('Positions')

