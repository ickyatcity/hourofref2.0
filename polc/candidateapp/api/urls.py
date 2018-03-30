from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    CandidatesWikiListAPIView,
    ScoreToggleUpAPIView
)

urlpatterns = [
      url(r'^$', CandidatesWikiListAPIView.as_view(), name='candidatelist'), 
      url(r'^(?P<slug>[\w-]+)/scoreup/$',ScoreToggleUpAPIView.as_view(), name='scoreup'),
      # url(r'^(?P<pk>\d+)/scorxeup/$', ScoreToggleUpAPIView.as_view(), name='scoreup'),
]
