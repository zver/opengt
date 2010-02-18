from django import template
register = template.Library()

from django.utils.translation import ugettext_lazy as _

@register.filter
def pretty_distance(distance):
	if not distance:
		return '-'
	distance = float(distance)
	km = distance/1000.
	return _('%1.2f km') % km

@register.filter
def pretty_timedelta(seconds):
	if not seconds:
		return '-'
	seconds = int(seconds)

	hours = int(seconds / 3600.)
	minutes = int((seconds - 3600*hours)/60.)
	return '%s:%02d' % (hours, minutes)
