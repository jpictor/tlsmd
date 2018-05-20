import re
import os
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, include
from django.views.generic.base import RedirectView
from rest_framework import routers
from . import views

admin.autodiscover()

urlpatterns = [
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', RedirectView.as_view(url='/admin/', permanent=False), name='index'),
]
