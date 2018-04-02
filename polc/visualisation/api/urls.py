# urls.py
from django.conf.urls import url

# from .views import graph, play_count_by_month
from .views import (
    CandidatesHistListAPIView
)




urlpatterns = [
    # url(r'^$', graph),
    # url(r'^api/play_count_by_month', play_count_by_month, name='play_count_by_month'),
    url(r'^(?P<id>\d+)$',CandidatesHistListAPIView.as_view(), name='scorehist'),
]