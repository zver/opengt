# vim: set fileencoding=utf-8 :
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate


def index(request):
	# FIXME: переделать логику на редиректы
	return render_to_response('agp/index.html', RequestContext(request))

@login_required
def map(request):
	return render_to_response('agp/map.html', RequestContext(request))

from django.contrib.auth.forms import AuthenticationForm
def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('trackers'))

	if request.POST:
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			auth_login(request, form.get_user())
			return HttpResponseRedirect(reverse('trackers'))
	else:
		form = AuthenticationForm()

	return render_to_response('agp/login.html', {'form': form}, RequestContext(request))

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login

def registration(request):
	return render_to_response('agp/registration.html', RequestContext(request))

def trackers(request):
	return render_to_response('agp/trackers.html', RequestContext(request))
	if request.POST:
		form = UserCreationForm(data=request.POST)
		if form.is_valid():
			user = form.save()

			password = request.POST['password1']
			user = authenticate(username=user.username, password=password)

			auth_login(request, user)
			return HttpResponseRedirect(reverse('trackers'))
	else:
		form = UserCreationForm()

	return render_to_response('agp/registration.html', {'form': form}, RequestContext(request))

def trackers(request):
	# FIXME
	form = None
	return render_to_response('agp/trackers.html', {'form': form}, RequestContext(request))


def kml_objects(request):
	if not request.user.is_authenticated():
		return HttpResponse()
	return HttpResponse()