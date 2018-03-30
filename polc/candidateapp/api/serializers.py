from django.utils.timesince import timesince
from rest_framework import serializers
from django.urls import reverse_lazy
from django.urls import reverse

# from accounts.api.serializers import UserDisplaySerializer
from candidateapp.models import CandidatesWiki



# class CandidateUserSerializer(serializers.ModelSerializer):
# 	 class Meta:
# 			model = CandidateUserRelx
# 			fields = [
# 				'users',
# 				]



class CandidateModelSerializer(serializers.ModelSerializer):
	 # urlreturn = serializers.SerializerMethodField()
	 class Meta:
			model = CandidatesWiki
			fields = [
				'candidate_id',
				'candiate_name',
				'title_wiki',
				'content_wiki',
				'references_wiki',
				'links_wiki',
				'sections_wiki',
				'summary_wiki',
				'fecha_ini_det',
				'fecha_ini_f',
				'score',
				'score_up',
				'score_down',
				# 'urlreturn',
				'slug',
				]


	 # def get_urlreturn(self, obj):
		# 	  return obj.get_absolute_url()


