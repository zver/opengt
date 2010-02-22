from django import forms
from tracker.models import Tracker

class TrackerForm(forms.ModelForm):
	def __init__(self, creator, *args, **kwargs):
		super(TrackerForm, self).__init__(*args, **kwargs)
		del self.fields['creator']
		self.creator = creator
		self.instance.creator = self.creator
	class Meta:
		model = Tracker
	def save(self, *args, **kwargs):
		self.instance.creator = self.creator
		super(TrackerForm, self).save(*args, **kwargs)

