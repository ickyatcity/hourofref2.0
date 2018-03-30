from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from candidateapp.models import CandidatesWiki, CandidateUserRelx


class graphAPIView(APIView):
    """
    A view that returns the count of active users in JSON.
    """
    # renderer_classes = (JSONRenderer, )

    def get(self, request, candidate_id, format=None):
    	graph = CandidatesWiki.objects.get(candidate_id=candidate_id)


    	return Response('i am here')




    # def get(self, request, slug, format=None):
    #     score_qs = CandidatesWiki.objects.get(slug=slug)
    #     user_qs = CandidateUserRelx.objects.all()

    #     message = "Not allowed"
    #     if request.user.is_authenticated():
    #         valid = score_qs.candidate_id
    #         finalscore = CandidateUserRelx.objects.score_toggle_up(request.user, score_qs, user_qs, slug)
    #         print 'finalscore here', finalscore
    #         # finalscore = '0'
    #         return Response({'finalscore': finalscore})
    #     return Response({"message": message}, status=400)
