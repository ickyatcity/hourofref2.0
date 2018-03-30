from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    graphAPIView
)

urlpatterns = [
      url(r'^(?P<candidate_id>\d+)/disp/$', graphAPIView.as_view(), name='graph'), 
]

