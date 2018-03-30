from django.db.models import Q
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response


from candidateapp.models import CandidatesWiki, CandidateUserRelx


from .pagination import StandardResultsPagination
from .serializers import CandidateModelSerializer


class ScoreToggleUpAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, slug, format=None):
        score_qs = CandidatesWiki.objects.get(slug=slug)
        user_qs = CandidateUserRelx.objects.all()

        message = "Not allowed"
        if request.user.is_authenticated:
            valid = score_qs.candidate_id
            finalscore = CandidateUserRelx.objects.score_toggle_up(request.user, score_qs, user_qs, slug)
            print ('finalscore here', finalscore)
            # finalscore = '0'
            return Response({'finalscore': finalscore})
        return Response({"message": message}, status=400)



class CandidatesWikiListAPIView(generics.ListAPIView):
    serializer_class = CandidateModelSerializer
    pagination_class = StandardResultsPagination

    def get_serializer_context(self, *args, **kwargs):
        context = super(CandidatesWikiListAPIView, self).get_serializer_context(*args, **kwargs)
        context['request'] = self.request
        return context
    
    def get_queryset(self, *args, **kwargs):
        
        # max_datetime = CandidatesWiki.objects.all().order_by('id')
        qs = CandidatesWiki.objects.all()

        query = self.request.GET.get("q", None)
        if query is not None:
            query = query.strip()
            qs = qs.filter( 
                Q(candiate_name__icontains=query) |
                Q(content_wiki__icontains=query) |
                Q(summary_wiki__icontains=query)
            )
        return qs 

    	
        # requested_user = self.kwargs.get("username")
        
        # if requested_user:
        #     qs = Tweet.objects.filter(user__username=requested_user).order_by("-timestamp")
        # else:
        #     im_following = self.request.user.profile.get_following() # none
        #     qs1 = Tweet.objects.filter(user__in=im_following)
        #     qs2 = Tweet.objects.filter(user=self.request.user)
        #     qs = (qs1 | qs2).distinct().order_by("-timestamp")
        
        # query = self.request.GET.get("q", None)
        # if query is not None:
        #     qs = qs.filter(
        #             Q(content__icontains=query) |
        #             Q(user__username__icontains=query)
        #             )
        # return qs

    # def get_queryset(self, *args, **kwargs):
        
    #     max_datetime = CandidatesWiki.objects.all().latest('fecha_ini_det')
    #     qs = CandidatesWiki.objects.all()

    #     query = self.request.GET.get("q", None)
    #     if query is not None:
    #         query = query.strip()
    #         qs = qs.filter( 
    #             Q(candiate_name__icontains=query) |
    #             Q(content_wiki__icontains=query) |
    #             Q(summary_wiki__icontains=query)
    #         )
    #     return qs



# class ScoreToggleUpAPIView(APIView):
#     # permission_classes = [permissions.IsAuthenticated]
#     def get(self, request, slug, format=None):
#         tweet_qs = Tweet.objects.filter(pk=pk)
#         # score_qs = CandidatesWiki.objects.filter(slug=slug)

#         # print 'user', user_qs
#         # print score_qs
#         # message = "Not allowed"
#         # if request.user.is_authenticated():
#             finalscore = CandidatesWiki.objects.score_toggle_up(request.user, )
#             return Response({'finalscore': finalscore})
#         # return Response({"message": message}, status=400)



# class LikeToggleAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request, pk, format=None):
#         tweet_qs = Tweet.objects.filter(pk=pk)
#         message = "Not allowed"
#         if request.user.is_authenticated():
#             is_liked = Tweet.objects.like_toggle(request.user, tweet_qs.first())
#             return Response({'liked': is_liked})
#         return Response({"message": message}, status=400)
