# vim: set fileencoding=utf-8 :
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

from tracker.models import Tracker


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
			return HttpResponseRedirect(reverse('map'))
	else:
		form = AuthenticationForm()

	return render_to_response('agp/login.html', {'form': form}, RequestContext(request))

from django.contrib.auth import logout as django_logout
def logout(request):
	django_logout(request)
	return HttpResponseRedirect(reverse('login'))

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
def registration(request):
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

@login_required
def trackers(request):
	from tracker.forms import TrackerForm
	trackers = Tracker.objects.filter(creator=request.user)
	if request.POST:
		form = TrackerForm(data=request.POST)
	else:
		form = TrackerForm()
	return render_to_response('agp/trackers.html', {	'trackers': trackers,
														'form':		form
													}, RequestContext(request))

@login_required
def del_tracker(request, tracker_id):
	qs = Tracker.objects.filter(pk=tracker_id)
	if qs.count() and qs[0].creator == request.user:
		qs.delete()
	return HttpResponseRedirect(reverse('trackers'))

@login_required
def edit_tracker(request, tracker_id):
	qs = Tracker.objects.filter(pk=tracker_id)
	if not qs.count() or qs[0].creator != request.user:
		return HttpResponseRedirect(reverse('trackers'))
	tracker = qs[0]
	return render_to_response('agp/tracker.html', {'tracker': tracker}, RequestContext(request))


