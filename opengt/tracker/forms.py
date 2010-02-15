from django import forms
from tracker.models import Tracker

class TrackerForm(forms.ModelForm):
	class Meta:
		model = Tracker
	
