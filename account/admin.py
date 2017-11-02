from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Account

admin.site.unregister(Group)
admin.site.register(Account)
