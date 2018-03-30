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
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


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
            print ('score_qs1',  score_qs.score_up - 1 )
            finalscore =   score_qs.score_up -1
            CandidatesWiki.objects.filter(slug=slug).update(
            score_up=finalscore)

        else:
            userload = CandidateUserRelx.objects.create(candidate_id=CandidatesWiki.objects.get(slug=slug) , users=user)
            finalscore =   score_qs.score_up + 1
            score_qs.score_up = finalscore
            CandidatesWiki.objects.filter(slug=slug).update(
            score_up=finalscore)
        
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
            print ( 'score_qs1',  score_qs.score_up - 1 )
            finalscore =   score_qs.score_up -1
            CandidatesWiki.objects.filter(slug=slug).update(
            score_up=finalscore)

        else:
            userload = CandidateUserRelx.objects.create(candidate_id=CandidatesWiki.objects.get(slug=slug) , users=user)
            finalscore =   score_qs.score_up + 1
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

    def get_absolute_url(self):
        return reverse("candidatesapp:candidatedetail", kwargs={"slug":self.slug})



class CandidateUserRelx(models.Model):
    candidate_id = models.ForeignKey(CandidatesWiki,  on_delete=models.CASCADE)
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    objects = CandidatesScoreManager()


class CandidateScoreHist(models.Model):
    candidate_id = models.ForeignKey(CandidatesWiki, on_delete=models.CASCADE)
    # candidate_id = models.ForeignKey(
    #     'CandidatesWiki',
    #     on_delete=models.CASCADE,
    # )
    score = models.IntegerField()
    timestamp   = models.DateTimeField(auto_now_add=True)
    updated     = models.DateTimeField(auto_now=True)





# @receiver(post_save, sender=CandidatesWiki, dispatch_uid=create_user_scorehist)
def create_user_scorehist(sender, instance, update_fields,  **kwargs):
    if 'score_up' in update_fields:
            CandidateScoreHist.objects.create(kwargs=['instance'])

            # instance.score = instance.candidate_id.score
    print ('I am here being updated')


post_save.connect(create_user_scorehist, sender=CandidatesWiki, dispatch_uid="create_user_scorehist")

# post_save.connect(create_user_scorehist, sender=CandidatesWiki)



    # @receiver(post_save, sender=CandidatesWiki)
    # def save_user_profile(sender, instance, update_fields=['score'] **kwargs):
    #     instance.profile.save()





   # from django.db.models.signals import post_save
   #  def default_subject(sender, instance, using):
   #      instance.price = instance.product.price
   #  pre_save.connect(default_subject, sender=Sell)


   #  # @receiver(post_save, sender=User)
    # def create_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    # instance.profile.save()


    # def save(self, *args, **kwargs):
    #     self.score = self.CandidatesWiki.score
    #     super(CandidateScoreHist, self).save(*args, **kwargs)




class Candidate(models.Model):
    cadidate    = models.CharField(max_length=225)
    cadidate_desc    = models.CharField(max_length=225)
    url_wiki = models.CharField(max_length=255, blank=True, null=True)
    title_wiki = models.CharField(max_length=255, blank=True, null=True)
    content_wiki = models.TextField(blank=True, null=True)
    images_wiki = models.TextField(blank=True, null=True)
    references_wiki = models.TextField(blank=True, null=True)
    links_wiki = models.TextField(blank=True, null=True)
    sections_wiki = models.TextField(blank=True, null=True)
    summary_wiki = models.TextField(blank=True, null=True)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.CASCADE)
    liked       = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')
    reply       = models.BooleanField(verbose_name='Is a reply?', default=False)
    updated     = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    score       = models.IntegerField()
    score_up    = models.IntegerField(settings.AUTH_USER_MODEL, blank=True)
    score_down  = models.IntegerField(settings.AUTH_USER_MODEL, blank=True)
    slug        = models.TextField(max_length=15)

    # objects = CandidatesUserManager()


    # def get_absolute_url(self):
    #     return reverse("candidatesapp:candidatedetail", kwargs={"slug":self.slug})

    def get_absolute_url(self):
        return reverse("candidatesapp:candidatedetail", kwargs={"pk":self.pk})


    class Meta:
        ordering = ['-timestamp']






                # if user in :
                #     print 'i am here'
                #         # user_obj.users.remove(user)
                #         # candidate_obj.score_up = candidate_obj.score_up - 1 
                #         # candidate_obj.score = candidate_obj.score_up
                #         # finalscore = candidate_obj.score
                # else:
                #         # user_obj.users.add(user)
                #         # candidate_obj.score_up = candidate_obj.score_up + 1
                #         # candidate_obj.score = candidate_obj.score_up
                #         # finalscore = candidate_obj.score
                #      print ' I am not here'   
 
                # user_obj.save()        
                # return finalscore



#     # def score_toggle_down(self, user, candidate_obj):
#     #         if user in candidate_obj.users.all():
#     #                 candidate_obj.users.remove(user)
#     #                 candidate_obj.score_down = candidate_obj.score_down - 1
#     #                 candidate_obj.score = candidate_obj.score_down
#     #                 finalscore = candidate_obj.score
#     #         else:
#     #                 candidate_obj.users.add(user)
#     #                 candidate_obj.score_down = candidate_obj.score_down + 1
#     #                 candidate_obj.score = candidate_obj.score_down
#     #                 finalscore = candidate_obj.score

#     #         candidate_obj.save()           
#     #         return finalscore

#     # def like_toggle(self, user, tweet_obj):
#     #     if user in tweet_obj.liked.all():
#     #         is_liked = False
#     #         tweet_obj.liked.remove(user)
#     #     else:
#     #         is_liked = True
#     #         tweet_obj.liked.add(user)
#     #     return is_liked

# class CandidatesUserManager(models.Manager):

#     def like_toggle(self, user):
      
#             is_liked = False
#             tweet_obj.liked.remove(user)
#         else:
#             is_liked = True
#             tweet_obj.liked.add(user)
#         return is_liked
