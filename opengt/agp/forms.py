from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegistrationForm(UserCreationForm):
	email = forms.EmailField(label="Email")
	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=commit)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user
