from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(label="Email")
	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=commit)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user


class StatForm(forms.Form):
	start_date = forms.DateTimeField(required=False, widget=AdminSplitDateTime())
	end_date = forms.DateTimeField(required=False, widget=AdminSplitDateTime())

