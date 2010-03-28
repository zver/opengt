# vim: set fileencoding=utf-8 :
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

from django_opengt.tracker.models import Tracker
from django_opengt.tracker.forms import TrackerForm


@login_required
def map(request):
	trackers = Tracker.objects.filter(creator=request.user)
	return render_to_response('map.html', {
					'trackers':	trackers,
			}, RequestContext(request))

@login_required
def statistics(request):
	from agp.forms import StatForm
	trackers = Tracker.objects.filter(creator=request.user)
	start_date = None
	end_date = None
	if request.POST:
		form = StatForm(data=request.POST)
		if form.is_valid():
			start_date = form.cleaned_data['start_date']
			end_date = form.cleaned_data['end_date']
	else:
		form = StatForm()

	for tr in trackers:
		tr.stats = tr.get_stats(start_date, end_date)

	return render_to_response('statistics.html', {
					'trackers': trackers,
					'form':	form,
			}, RequestContext(request))

from django.contrib.auth.forms import AuthenticationForm
def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('trackers'))
	next = request.REQUEST.get('next', reverse('map'))

	if request.POST:
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			auth_login(request, form.get_user())
			return HttpResponseRedirect(next)
	else:
		form = AuthenticationForm()

	return render_to_response('login.html', {
													'form': form,
													'next': next,
												}, RequestContext(request))

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

	return render_to_response('registration.html', {'form': form}, RequestContext(request))

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

	return render_to_response('trackers.html', {	'trackers': trackers,
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
	return render_to_response('edit_tracker.html', {
										'tracker'	: tracker,
										'form'		: form,
										}, RequestContext(request))


