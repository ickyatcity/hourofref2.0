# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.urls import reverse
from django.db import models
from django.db.models import F
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

# signals - this is to update the score history when master table is updated.
import django.dispatch
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.dispatch import Signal
from .signals import user_attributes_changed


'''
===========================================================
                             REFERENCES 
===========================================================

Signals - 

https://medium.com/@adriennedomingus/signals-in-django-24b6a945cd97
https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#onetoone
https://simpleisbetterthancomplex.com/tutorial/2016/07/28/how-to-create-django-signals.html
https://docs.djangoproject.com/en/2.0/topics/signals/#receiver-functions
https://stackoverflow.com/questions/13014411/django-post-save-signal-implementation
http://sabinemaennel.ch/django/signals-in-django/

Model Manager - 
https://docs.djangoproject.com/en/2.0/topics/db/managers/

Model - 
https://docs.djangoproject.com/en/2.0/ref/models/instances/

'''


class CandidatesScoreManager(models.Manager):
    def score_toggle_up(self, user, candidate_obj, user_obj, slug):
        # finalscore = 0  
        # CandidatesWiki.objects.update(
        # score_up=finalscore)

        try:
            user_qs = CandidateUserRelx.objects.get(candidate_id=candidate_obj.candidate_id)
            score_qs = CandidatesWiki.objects.get(candidate_id=candidate_obj.candidate_id)
        except CandidateUserRelx.DoesNotExist:
            user_qs = None
            score_qs = CandidatesWiki.objects.get(candidate_id=candidate_obj.candidate_id)

        if user_qs:
            userload = CandidateUserRelx.objects.filter(users=user).delete()
            print ('score_qs1', score_qs.score_up - 1)
            finalscore = score_qs.score_up - 1
            candidatewiki = CandidatesWiki.objects.filter(slug=slug).update(
                score_up=finalscore)

            CandidatesWiki().save()
            user_attributes_changed.send(sender=self.__class__, candidate_id=candidate_obj.candidate_id, score_up=finalscore)


        else:
            userload = CandidateUserRelx.objects.create(candidate_id=CandidatesWiki.objects.get(slug=slug), users=user)
            finalscore = score_qs.score_up + 1
            score_qs.score_up = finalscore
            candidatewiki = CandidatesWiki.objects.filter(slug=slug).update(
                score_up=finalscore)

            CandidatesWiki().save()
            user_attributes_changed.send(sender=self.__class__, candidate_id=candidate_obj.candidate_id, score_up=finalscore)


        return finalscore

    def score_toggle_down(self, user, candidate_obj, user_obj, slug):
        # finalscore = 0  
        # CandidatesWiki.objects.update(
        # score_up=finalscore)

        try:
            user_qs = CandidateUserRelx.objects.get(candidate_id=candidate_obj.candidate_id)
            score_qs = CandidatesWiki.objects.get(candidate_id=candidate_obj.candidate_id)
        except CandidateUserRelx.DoesNotExist:
            user_qs = None
            score_qs = CandidatesWiki.objects.get(candidate_id=candidate_obj.candidate_id)

        if user_qs:
            userload = CandidateUserRelx.objects.filter(users=user).delete()
            print ('score_qs1', score_qs.score_up - 1)
            finalscore = score_qs.score_up - 1
            CandidatesWiki.objects.filter(slug=slug).update(
                score_up=finalscore)

        else:
            userload = CandidateUserRelx.objects.create(candidate_id=CandidatesWiki.objects.get(slug=slug), users=user)
            finalscore = score_qs.score_up + 1
            score_qs.score_up = finalscore
            CandidatesWiki.objects.filter(slug=slug).update(
                score_up=finalscore)
        return finalscore


class CandidatesWiki(models.Model):
    candidate_id = models.AutoField(primary_key=True)
    candiate_name = models.CharField(max_length=255)
    url_wiki = models.CharField(max_length=255, blank=True, null=True)
    title_wiki = models.CharField(max_length=255, blank=True, null=True)
    content_wiki = models.TextField(blank=True, null=True)
    images_wiki = models.TextField(blank=True, null=True)
    references_wiki = models.TextField(blank=True, null=True)
    links_wiki = models.TextField(blank=True, null=True)
    sections_wiki = models.TextField(blank=True, null=True)
    summary_wiki = models.TextField(blank=True, null=True)
    fecha_ini_det = models.DateTimeField(blank=True, null=False)
    fecha_ini_f = models.DateField(blank=True, null=False)
    score = models.IntegerField()
    score_up = models.IntegerField(settings.AUTH_USER_MODEL, blank=True)
    score_down = models.IntegerField(settings.AUTH_USER_MODEL, blank=True)
    slug = models.TextField(max_length=15)

    objects = CandidatesScoreManager()

    class Meta:
        managed = False
        db_table = 'candidates_wiki'
        get_latest_by = 'fecha_ini_det'
        ordering = ['candiate_name']

    def get_absolute_url(self):
        return reverse("candidatesapp:candidatedetail", kwargs={"slug": self.slug})


class CandidateUserRelx(models.Model):
    candidate_id = models.ForeignKey(CandidatesWiki, on_delete=models.CASCADE)
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = CandidatesScoreManager()



class CandidateScoreHistManager(models.Manager):
    def create_score_entry(self, candidate_id, score):
        score_entry = self.create(candidate_id = candidate_id, score=score)
        return score_entry




class CandidateScoreHist(models.Model):
    candidate_id = models.CharField(max_length=255)
    score = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CandidateScoreHistManager()




@receiver(user_attributes_changed)
def create_user_scorehist(sender, candidate_id, score_up, **kwargs):

    scorechange = CandidateScoreHist.objects.create_score_entry(candidate_id, score_up)
    scorechange.save()

    print ('I am here being updated',score_up)




class Candidate(models.Model):
    cadidate = models.CharField(max_length=225)
    cadidate_desc = models.CharField(max_length=225)
    url_wiki = models.CharField(max_length=255, blank=True, null=True)
    title_wiki = models.CharField(max_length=255, blank=True, null=True)
    content_wiki = models.TextField(blank=True, null=True)
    images_wiki = models.TextField(blank=True, null=True)
    references_wiki = models.TextField(blank=True, null=True)
    links_wiki = models.TextField(blank=True, null=True)
    sections_wiki = models.TextField(blank=True, null=True)
    summary_wiki = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')
    reply = models.BooleanField(verbose_name='Is a reply?', default=False)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField()
    score_up = models.IntegerField(settings.AUTH_USER_MODEL, blank=True)
    score_down = models.IntegerField(settings.AUTH_USER_MODEL, blank=True)
    slug = models.TextField(max_length=15)

    # objects = CandidatesUserManager()

    # def get_absolute_url(self):
    #     return reverse("candidatesapp:candidatedetail", kwargs={"slug":self.slug})

    def get_absolute_url(self):
        return reverse("candidatesapp:candidatedetail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ['-timestamp']
