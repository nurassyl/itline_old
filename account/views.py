from django.shortcuts import render
from django.http import JsonResponse, Http404
from account.models import Account
from django.forms.models import model_to_dict
from django.db import IntegrityError
from django.core.exceptions import ValidationError

def root(req):
	if req.method == 'GET':
		try:
			user = Account.objects.create_superuser(name=' nurasyl aldan ', email='nurassyl.aldan1@gmail.com', password='12345')
		except IntegrityError:
			return JsonResponse({'message': 'email is exists'})
		#user = Account.objects.get(pk=10)
		data = model_to_dict(user)
		return JsonResponse(data, safe=False)
	elif req.method == 'POST':
		# Create.
		data = {}
		return JsonResponse(data, safe=False)
	elif req.method == 'DELETE':
		# Delete.
		data = {}
		return JsonResponse(data, safe=False)
	elif req.method == 'PUT':
		# Delete.
		data = {}
		return JsonResponse(data, safe=False)
	else:
		raise Http404
