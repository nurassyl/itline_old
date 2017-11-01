from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import check_password
from account.models import Account

class Session(object):
	@classmethod
	def authenticate(csl, email=None, password=None):
		try:
			account = Account()
			account.email = email
			account.password = password
			account.normalize()

			user = Account.objects.get(email=account.email)
			user.check_password(account.password)
			return user
		except Account.DoesNotExist:
			return None
