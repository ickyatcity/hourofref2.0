from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from .views import settings, password, signup
# from .views import activate, account_activation_sent


from .views import (
    UserDetailView
)





urlpatterns = [
      url(r'^settings/$', settings, name='settings'),
      url(r'^settings/password/$', password, name='password'),
      url(r'^signup/$', signup, name='signup'),
      url(r'^(?P<username>[\w.@+-]+)/$', UserDetailView.as_view(), name='profile'), 
      # url(r'^account_activation_sent/$', account_activation_sent, name='account_activation_sent'),
      # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
      #  activate, name='activate'),
]
