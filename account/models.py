from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from itline import settings
import re
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError
from datetime import datetime
import time

def validate_language(value):
	if value not in settings.LANGUAGES:
		return settings.LANGUAGE_CODE

class AccountManager(BaseUserManager):
	def create_account(self, name, email, password, language=None, ip=None, user_agent=None):
		user = self.model()
		user.name = name
		user.email = email
		user.password = password
		user.normalize()
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
	REQUIRED_FIELDS = ['password', 'name']

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

	recovery_token = models.CharField(max_length=100, null=True, blank=True, default=None)
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
	created_country = models.CharField(max_length=100, null=True, blank=True, default=None)
	created_region = models.CharField(max_length=100, null=True, blank=True, default=None)
	created_city = models.CharField(max_length=100, null=True, blank=True, default=None)
	created_timezone = models.CharField(max_length=100, null=True, blank=True, default=None)
	created_isp = models.CharField(max_length=250, null=True, blank=True, default=None)

	created_user_agent = models.CharField(max_length=300, null=True, blank=True, default=None)
	created_browser_family = models.CharField(max_length=50, null=True, blank=True, default=None)
	created_browser_version = models.CharField(max_length=25, null=True, blank=True, default=None)
	created_os_family = models.CharField(max_length=50, null=True, blank=True, default=None)
	created_os_version = models.CharField(max_length=25, null=True, blank=True, default=None)
	created_device_family = models.CharField(max_length=50, null=True, blank=True, default=None)
	created_device_brand = models.CharField(max_length=50, null=True, blank=True, default=None)
	created_device_model = models.CharField(max_length=50, null=True, blank=True, default=None)
	created_device_type = models.CharField(max_length=25, null=True, blank=True, default=None)

	def normalize_email(self):
		self.email = self.email.strip().lower()
	def normalize_password(self):
		self.password = self.password.strip()
	def normalize(self):
		self.normalize_email()
		self.normalize_password()
		self.name = self.name.strip(); self.name = re.sub('\s+', ' ', self.name); self.name = self.name.title()

	def set_login_time(self):
		self.login_datetime = datetime.now()
		self.login_time = int(time.time())
		self.save()
	def  activate(self):
		self.is_active = True
		self.save()
	def  deactivate(self):
		self.is_active = False
		self.save()
	def to_administer(self):
		self.is_admin = True
		self.save()
	def to_deadminister(self):
		self.is_admin = False
		self.save()
