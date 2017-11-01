from django.shortcuts import render
from django.http import JsonResponse, Http404
from account.models import Account
from django.forms.models import model_to_dict
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db import connection

def root(req):
	if req.method == 'POST':
		try:
			transaction.set_autocommit(False)
			with transaction.atomic():
				user = Account.objects.create_superuser(name=req.POST.get('name', ''), email=req.POST.get('email', ''), password=req.POST.get('password', ''), language=req.POST.get('language', ''))
				data = model_to_dict(user)
			transaction.commit()
			# print(connection.queries)
			return JsonResponse(data, safe=False, status=201)
		except ValidationError as error:
			return JsonResponse(error.message_dict, safe=False, status=400)
	elif req.method == 'DELETE':
		# Delete.
		data = {}
		return JsonResponse(data, safe=False)
	elif req.method == 'PUT':
		# Update.
		data = {}
		return JsonResponse(data, safe=False)
	else:
		raise Http404
