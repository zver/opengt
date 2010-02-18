# vim: set fileencoding=utf-8 :
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

from tracker.models import Tracker
from tracker.forms import TrackerForm


def index(request):
	return HttpResponseRedirect(reverse('trackers'))

@login_required
def map(request):
	return render_to_response('agp/map.html', RequestContext(request))

@login_required
def statistics(request):
	trackers = Tracker.objects.filter(creator=request.user)
	return render_to_response('agp/statistics.html', {'trackers': trackers}, RequestContext(request))

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

from agp.forms import RegistrationForm
from django.contrib.auth import login as auth_login
def registration(request):
	if request.POST:
		form = RegistrationForm(data=request.POST)
		if form.is_valid():
			user = form.save()

			password = request.POST['password1']
			user = authenticate(username=user.username, password=password)

			auth_login(request, user)
			return HttpResponseRedirect(reverse('trackers'))
	else:
		form = RegistrationForm()

	return render_to_response('agp/registration.html', {'form': form}, RequestContext(request))

@login_required
def trackers(request):
	trackers = Tracker.objects.filter(creator=request.user)
	if request.POST:
		form = TrackerForm(data=request.POST, creator=request.user)
		if form.is_valid():
			new_tracker = form.save()
			form = TrackerForm(creator=request.user)
	else:
		form = TrackerForm(creator=request.user)

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
	if request.POST:
		form = TrackerForm(instance=tracker, data=request.POST, creator=request.user)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('trackers'))
	form = TrackerForm(instance=tracker, creator=request.user)
	return render_to_response('agp/edit_tracker.html', {
										'tracker'	: tracker,
										'form'		: form,
										}, RequestContext(request))


