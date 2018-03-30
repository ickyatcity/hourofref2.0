# Create your views here.
from __future__ import unicode_literals
from django import forms
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy, reverse

from django.views.generic import (
    DeleteView,
    DetailView, 
    ListView, 
    CreateView, 
    FormView,
    UpdateView
)

# Model Import 
# from .forms import PoliticianModelForm
from .models import (
    CandidatesWiki
   )


class CandidateListView(ListView):

    template_name = 'politicians/search_result.html'

    def get_queryset(self, *args, **kwargs):
        
        # max_datetime = CandidatesWiki.objects.all().latest('fecha_ini_det')
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




    def get_context_data(self, *args, **kwargs):
        context = super(CandidateListView, self).get_context_data(*args, **kwargs)
        return context


class CandidateDetailView(DetailView):
    template_name = 'politicians/politician_detail.html'
    queryset = CandidatesWiki.objects.all()

