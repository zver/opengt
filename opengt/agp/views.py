# vim: set fileencoding=utf-8 :
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
	# FIXME: переделать логику на редиректы
	return render_to_response('agp/index.html', RequestContext(request))

def map(request):
	return render_to_response('agp/map.html', RequestContext(request))
