from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.root),
    url(r'^sessions$', views.sessions),
    url(r'^recovery$', views.recovery)
]
