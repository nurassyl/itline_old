from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, Http404
from account.models import Account
from django.forms.models import model_to_dict
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db import transaction
from django.contrib.auth import login, logout, authenticate

@transaction.atomic
def root(req):
	if req.method == 'POST':
		try:
			user = Account.objects.create_account(name=req.POST.get('name', None), email=req.POST.get('email', None), password=req.POST.get('password', None), language=req.POST.get('language', None), ip=req.META.get('REMOTE_ADDR', None), user_agent=req.META.get('HTTP_USER_AGENT', None))
			return JsonResponse(model_to_dict(user), safe=False, status=201)
		except ValidationError as error:
			return JsonResponse(error.message_dict, safe=False, status=400)
	elif req.method == 'DELETE':
		# Delete.
		return JsonResponse({}, safe=False)
	elif req.method == 'PUT':
		# Update.
		return JsonResponse({}, safe=False)
	else:
		raise Http404

@transaction.atomic
def sessions(req):
	if req.method == 'POST':
		account = authenticate(req, username=req.POST.get('email', ''), password=req.POST.get('password', ''))
		if account is not None:
			login(req, account)
			return HttpResponse('', content_type='text/plain', status=202)
		else:
			# Email or password is invalid.
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
