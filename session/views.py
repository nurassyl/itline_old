from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.auth import login, logout
from session.models import Session

def root(req):
	if req.method == 'POST':
		account = Session.authenticate(email=req.POST.get('email', ''), password=req.POST.get('password', ''))
		if account is not None:
			login(req, account)
			return HttpResponse('', content_type='text/plain', status=202)
		else:
			raise Http404
	elif req.method == 'DELETE':
		logout(req)
		return HttpResponse('', content_type='text/plain', status=202)
	else:
		raise Http404
