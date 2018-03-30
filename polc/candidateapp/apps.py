# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class CandidateappConfig(AppConfig):
    name = 'candidateapp'
    label = 'candidateapp'

def ready(self):
    import name.signals