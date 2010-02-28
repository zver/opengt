import datetime
from django.conf import settings

def get_segments(positions_qs):
	""" Split positions_qs to lists by settings.MIN_LINK_TIMEOUT """
	segments = []
	seg = []
	prev_pos = None
	for pos in positions_qs:
		if not prev_pos:
			prev_pos = pos
			continue
		time_delta = (pos.date-prev_pos.date).seconds
		if time_delta < settings.MIN_LINK_TIMEOUT:
			seg.append(pos)
		else:
			if len(seg) > 1:
				segments.append(seg)
			seg = [pos]
		prev_pos = pos
	if len(seg) > 1:
		segments.append(seg)
	return segments
		
