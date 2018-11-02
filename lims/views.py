import os
import sys
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import SequencingSample, SequencingSampleSheet, SequencingRun
# import 'util' from top level directory
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, parentdir)
from util import find
sys.path.pop(0)



def index(request):
    latest_runs = SequencingRun.objects.order_by('id')[:5]
    latest_samples = SequencingSample.objects.order_by('id')[:5]
    latest_samplesheets = SequencingSampleSheet.objects.order_by('id')[:5]
    return render(request, 'lims/index.html', {'latest_runs': latest_runs, 'latest_samples': latest_samples, 'latest_samplesheets': latest_samplesheets})

class RunsList(generic.ListView):
    template_name = 'lims/runs_list.html'
    context_object_name = 'runs'

    def get_queryset(self):
        """Return the last five runs """
        return SequencingRun.objects.order_by('id')[:5]

class SampleSheetList(generic.ListView):
    template_name = 'lims/samplesheets_list.html'
    context_object_name = 'samplesheets'

    def get_queryset(self):
        """Return the last five samplesheets """
        return SequencingSampleSheet.objects.order_by('id')[:5]

class SamplesList(generic.ListView):
    template_name = 'lims/samples_list.html'
    context_object_name = 'samples'

    def get_queryset(self):
        """Return the last five samples """
        return SequencingSample.objects.order_by('id')[:5]

class SampleDetail(generic.DetailView):
    pk_url_kwarg = 'id'
    model = SequencingSample
    context_object_name = 'sample'
    template_name = 'lims/sample_detail.html'

class RunDetail(generic.DetailView):
    pk_url_kwarg = 'id'
    model = SequencingRun
    context_object_name = 'run'
    template_name = 'lims/run_detail.html'

class SampleSheetDetail(generic.DetailView):
    pk_url_kwarg = 'id'
    model = SequencingSampleSheet
    context_object_name = 'samplesheet'
    template_name = 'lims/samplesheet_detail.html'
