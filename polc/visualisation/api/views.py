from django.core import serializers
from django.forms.models import model_to_dict
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response

from candidateapp.models import CandidateScoreHist

from .serializers import CandidateScoreHistModelSerializer


class CandidatesHistListAPIView(APIView):

    def get(self, request, id):
        scorehist_qs = CandidateScoreHist.objects.get(id=id)
        data = model_to_dict(scorehist_qs)
        data = 0
        return Response({'scorehist': data})


#
# class CandidatesHistListAPIView(APIView):
#     scorehist_qs = CandidateScoreHist.objects.get(candidate_id=candidate_id)
#     serializer_class = TestSerializer
#
#
#
# def getObject(request, id):
#     obj = MyModel.objects.get(pk=id)
#     data = serializers.serialize('json', [obj,])
#     struct = json.loads(data)
#     data = json.dumps(struct[0])
#     return HttpResponse(data, mimetype='application/json')
#


    # serializer_class = CandidateScoreHistModelSerializer
    # scorehist_qs = CandidateScoreHist.objects.get(candidate_id=candidate_id)
    #
    # def get_serializer_context(self, *args, **kwargs):
    #     context = super(CandidatesHistListAPIView, self).get_serializer_context(*args, **kwargs)
    #     context['request'] = self.request
    #     return context
    #
    # # def get(self, request, candidate_id):
    # #     scorehist_qs = CandidateScoreHist.objects.get(candidate_id=candidate_id)
    # #
    # #
    # #     return scorehist_qs
    #
    #
    # def get(self, request, *args, **kwargs):
    #    self.object = self.get_object()
    #    return Response({'user': self.object}, template_name='user_detail.html')
    #
    #
    #


# def graph(request):
#     return render(request, 'visualisation/graph.html')
#
#
# def play_count_by_month(request):
#     data = CandidateScoreHist.objects.all()
#     return JsonResponse(list(data), safe=False)