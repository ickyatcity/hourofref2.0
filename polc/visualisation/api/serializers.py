from django.utils.timesince import timesince
from rest_framework import serializers
from django.urls import reverse_lazy
from django.urls import reverse

# from accounts.api.serializers import UserDisplaySerializer
from candidateapp.models import CandidateScoreHist


class CandidateScoreHistModelSerializer(serializers.ModelSerializer):
    # jsonfield = serializers.SerializerMethodField()
    class Meta:
        model = CandidateScoreHist
        fields = [
            'candidate_id',
            'score',
            'timestamp',
            'updated ',
        ]
    #
    # def get_jsonfield(self, obj):
    # 	  return obj.get_absolute_url()