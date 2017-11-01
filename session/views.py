from django.shortcuts import render
from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.forms.models import model_to_dict

def root(req):
	if req.method == 'POST':
		account = authenticate(req, username=req.POST.get('email', ''), password=req.POST.get('password', ''))
		if account is not None:
			login(req, account)
			return HttpResponse('', content_type='text/plain', status=202)
		else:
			raise Http404
	elif req.method == 'DELETE':
		logout(req)
		return HttpResponse('', content_type='text/plain', status=202)
	elif req.method == 'GET':
		if req.user.is_anonymous():
			return HttpResponse('', content_type='text/plain', status=401)
		else:
			return JsonResponse(model_to_dict(req.user))
	else:
		raise Http404
