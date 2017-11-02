from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from itline import settings
import re
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
import time
from django.utils import timezone

def validate_language(value):
	if value not in settings.LANGUAGES:
		return settings.LANGUAGE_CODE

class AccountManager(BaseUserManager):
	def create_account(self, name, email, password, language=None, ip=None, user_agent=None):
		user = self.model()
		user.name = Account.normalize_name(name)
		user.email = Account.normalize_email(email)
		user.password = Account.normalize_password(password)
		user.created_ip = ip
		user.created_user_agent = user_agent
		user.full_clean()
		user.set_password(password)
		user.save(using=self._db)
		return user
	def create_superuser(self, name, email, password, language=None, ip=None, user_agent=None):
		user = self.create_account(name=name, email=email, password=password, language=language, ip=ip, user_agent=user_agent)
		user.is_admin = True
		user.save(using=self._db)
		return user

class Account(AbstractBaseUser):
	class Meta:
		db_table = 'accounts'
	objects = AccountManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name']

	def __str__(self):
		return self.email
	def get_full_name(self):
		return self.name
	def get_short_name(self):
		return self.email
	def has_perm(self, perm, obj=None):
		return True
	def has_module_perms(self, app_label):
		return True
	@property
	def is_staff(self):
		return self.is_admin

	email = models.EmailField(unique=True, max_length=254, validators=[MinLengthValidator(5)])
	password = models.SlugField(max_length=100, validators=[MinLengthValidator(6)])

	recovery_token = models.CharField(unique=True, max_length=100, null=True, blank=True, default=None)
	recovery_token_expire = models.IntegerField(null=True, blank=True, default=None)

	login_datetime = models.DateTimeField(auto_now=True)
	login_time = models.IntegerField(default=int(time.time()))

	name = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
	language = models.CharField(max_length=5, default=settings.LANGUAGE_CODE, validators=[validate_language])
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	created_datetime = models.DateTimeField(auto_now=True)
	created_time = models.IntegerField(default=int(time.time()))

	created_ip = models.GenericIPAddressField(null=True, blank=True, default=None)
	created_location = models.CharField(max_length=200, null=True, blank=True, default=None)
	created_user_agent = models.CharField(max_length=300, null=True, blank=True, default=None)

	@classmethod
	def normalize_email(cls, value):
		value = value.strip().lower()
		return value
	@classmethod
	def normalize_password(cls, value):
		value = value.strip()
		return value
	@classmethod
	def normalize_name(csl, value):
		value = value.strip(); value = re.sub('\s+', ' ', value); value = value.title()
		return value

	def set_login_time(self):
		self.login_datetime = timezone.now()
		self.login_time = int(time.time())
		self.save()
