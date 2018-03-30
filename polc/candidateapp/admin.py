# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib import admin

# Register your models here.
# from .forms import CandidateModelForm
from .models import Candidate


#admin.site.register(Tweet)


class TweetModelAdmin(admin.ModelAdmin):
    #form = TweetModelForm
    class Meta:
        model = Candidate
        


# admin.site.register(Tweet, TweetModelAdmin)