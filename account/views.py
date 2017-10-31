from django.shortcuts import render
from django.http import JsonResponse, Http404

def root(req):
	if req.method == 'GET':
		data = {}
		return JsonResponse(data, safe=False)
	elif req.method == 'POST':
		data = {}
		return JsonResponse(data, safe=False)
	else:
		raise Http404
