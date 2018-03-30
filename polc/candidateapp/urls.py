from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    CandidateListView,
    CandidateDetailView
)


urlpatterns = [
      url(r'^$', RedirectView.as_view(url='/')), 
      url(r'^search/$', CandidateListView.as_view(), name='candidatelist'), 
      # url(r'^(?P<pk>\d+)/$', PolitDetailView.as_view(), name='politdetail'), 
      url(r'^(?P<slug>[\w-]+)/$',CandidateDetailView.as_view(), name='candidatedetail'),
]
