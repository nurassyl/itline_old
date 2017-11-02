from django.http import JsonResponse, HttpResponse, Http404
from account.models import Account
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from django.db import transaction

@transaction.atomic
def root(req):
	if req.method == 'POST':
		# Create.
		try:
			user = Account.objects.create_account(name=req.POST.get('name', None), email=req.POST.get('email', None), password=req.POST.get('password', None), language=req.POST.get('language', None), ip=req.META.get('REMOTE_ADDR', None), user_agent=req.META.get('HTTP_USER_AGENT', None))
			return JsonResponse(model_to_dict(user), status=201)
		except ValidationError as error:
			return JsonResponse(error.message_dict, status=400)
	elif req.method == 'DELETE':
		# Delete.
		return JsonResponse({})
	elif req.method == 'PUT':
		# Update.
		return JsonResponse({})
	else:
		raise Http404

@transaction.atomic
def sessions(req):
	from django.contrib.auth import login, logout, authenticate

	if req.method == 'POST':
		email = Account.normalize_email(req.POST.get('email', ''))
		password = Account.normalize_password(req.POST.get('password', ''))
		account = authenticate(req, username=email, password=password)
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

@transaction.atomic
def recovery(req):
	import re
	import time
	import uuid

	if req.method == 'GET':
		email = Account.normalize_email(req.GET.get('email', ''))
		try:
			account = Account.objects.get(email=email)
			account.recovery_token = re.sub('-', '', str(uuid.uuid4()))
			account.recovery_token_expire = int(time.time()+300) # 5 minutes.
			account.save()
			data = {
				'id': account.id,
				'email': account.email,
				'old_password_hash': account.password,
				'recovery_token': account.recovery_token,
				'recovery_token_expire': account.recovery_token_expire
			}
			# send 'data' to email address.
			return HttpResponse('', content_type='text/plain', status=200)
		except Account.DoesNotExist:
			raise Http404
	elif req.method == 'POST':
		password = Account.normalize_password(req.POST.get('password', ''))
		token = req.POST.get('token')
		try:
			account = Account.objects.get(recovery_token=token)
			if int(time.time()) > account.recovery_token_expire:
				# Timeout.
				account.recovery_token = None
				account.recovery_token_expire = None
				account.save()
				return HttpResponse('', content_type='text/plain', status=408)
			else:
				account.password = password
				try:
					account.full_clean()
				except ValidationError as error:
					return JsonResponse(error.message_dict, status=400)
				account.set_password(password)
				account.recovery_token = None
				account.recovery_token_expire = None
				account.save()
				account.session_set.all().delete()
				return HttpResponse('', content_type='text/plain', status=202)
		except Account.DoesNotExist:
			raise Http404
	else:
		raise Http404
