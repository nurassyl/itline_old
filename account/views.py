from django.shortcuts import render
from django.http import JsonResponse, Http404
from account.models import Account
from django.forms.models import model_to_dict
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db import connection

def root(req):
	if req.method == 'GET':
		transaction.set_autocommit(False)
		try:
			with transaction.atomic():
				user = Account.objects.create_account(name=' nurasyl aldan ', email='nurassyl.aldan@gmail.com', password='nurasyl12345')
				data = model_to_dict(user)
			transaction.commit()
			# print(connection.queries)
			return JsonResponse(data, safe=False)
		except ValidationError as error:
			return JsonResponse(error.message_dict, safe=False)
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
