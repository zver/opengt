from django import forms
from django.conf import settings
from django.db import models


class ColorWidget(forms.widgets.Input):
	class Media:
		js = [settings.MEDIA_URL + "js/jscolor/jscolor.js"]
		
	def render(self, name, value, attrs={}):
		attrs['class'] = (attrs.get('class', '') + ' color').strip()
		return super(ColorWidget, self).render(name, value, attrs=attrs)

		
class ColorField(models.CharField):
	def __init__(self, *args, **kwargs):
		kwargs['max_length'] = 6
		super(ColorField, self).__init__(*args, **kwargs)

	def formfield(self, **kwargs):
		kwargs['widget'] = ColorWidget
		return super(ColorField, self).formfield(**kwargs)
