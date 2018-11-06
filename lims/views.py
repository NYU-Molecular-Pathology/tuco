import os
import sys
import datetime
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import now
from django.forms.models import model_to_dict

from .models import SequencingSample, SequencingSampleSheet, SequencingRun
from .forms import SequencingSampleSheetForm

# import 'util' from top level directory
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, parentdir)
from util import find, samplesheet
sys.path.pop(0)


def samplesheet_upload(request):
    template = 'lims/samplesheet_upload.html'
    form = SequencingSampleSheetForm()
    message = ''
    context = {'form': form, 'message': message}
    if request.method == 'POST' and request.FILES['samplesheet']:
        # print(dir(request))
        run_id = request.POST['run_id']
        sheet = request.FILES['samplesheet']

        # set up temp storage location for file; needed for samplesheet module read methods..
        # MEDIA_TMP/<timestamp>/filename
        fs = FileSystemStorage()
        tmp_save_path = os.path.join(
        settings.MEDIA_TMP,
        datetime.datetime.strftime(now(), '%Y-%m-%d'),
        sheet.name
        )

        # save file to disk at location
        filename = fs.save(tmp_save_path, sheet)
        uploaded_file_url = fs.url(filename)

        # try to parse the file as a SampleSheet.csv file
        try:
            sheet_obj = samplesheet.IEMFile(path = os.path.realpath(filename))
        except:
            context['message'] = "ERROR: Samplesheet file could not be parsed. Is it in the correct format?"
            return render(request, template, context, status = 422)

        # validate the contents of the samplesheet
        try:
            sheet_obj.isValid(_raise = True)
        except:
            context['message'] = "ERROR: Samplesheet contains errors;\n{0}".format(json.dumps([ {k:v} for k, v, in sheet_obj.get_validations().items() if v ]))
            return render(request, template, context, status = 422)

        # make sure the sheet is not already in the databse
        num_matches = SequencingSampleSheet.objects.filter(md5 = sheet_obj.md5).count()
        if num_matches > 0:
            context['message'] = "ERROR: This exact samplesheet has already been uploaded, please re-assign the existing version instead."
            return render(request, template, context, status = 409)

        # try to put the samplesheet into the database
        try:
            sheet_instance = SequencingSampleSheet.objects.create(
            run_id =  SequencingRun.objects.get(run_id = run_id),
            file = sheet,
            md5 = sheet_obj.md5,
            host = sheet_obj.meta.get('Sheet_host', '')
            )
        except:
            context['message'] = "ERROR: Samplesheet could not be imported into the database."
            return render(request, template, context, status = 422)

        # try to import samples from the samplesheet
        try:
            all_created = []
            not_created = []
            for record in sheet_obj.flatten():
                instance, created = SequencingSample.objects.get_or_create(
                    run_id = SequencingRun.objects.get(run_id = run_id),
                    sample = record.get('Sample_ID',''),
                    sample_name = record.get('Sample_Name',''),
                    # paired_normal = record.get('Paired_Normal',''), # get this separately!
                    i7_index = record.get('I7_Index_ID',''),
                    index = record.get('index',''),
                    sample_project = record.get('Sample_Project',''),
                    description = record.get('Description',''),
                    genome_folder = record.get('GenomeFolder',''),
                    samplesheet = sheet_instance
                    )
                if created:
                    all_created.append((instance, created))
                if not created:
                    not_created.append((instance, created))
            context['message'] = "The following samples from the samplesheet were successfully imported:\n{0}\n\nThe following samples were not successfully imported:\n{1}".format(
            '\n'.join([i[0].__str__() for i in all_created]),
            '\n'.join([i[0].__str__() for i in not_created])
            )
            return render(request, template, context)
        except:
            context['message'] = "ERROR: An error occured while importing samples from the samplesheet into the database."
            return render(request, template, context, status = 422)
    else:
        return render(request, template, context)

def index(request):
    latest_runs = SequencingRun.objects.order_by('imported')[:5]
    latest_samples = SequencingSample.objects.order_by('imported')[:5]
    latest_samplesheets = SequencingSampleSheet.objects.order_by('imported')[:5]
    return render(request, 'lims/index.html', {'latest_runs': latest_runs, 'latest_samples': latest_samples, 'latest_samplesheets': latest_samplesheets})

class RunsList(generic.ListView):
    template_name = 'lims/runs_list.html'
    context_object_name = 'runs'

    def get_queryset(self):
        """Return the last five runs """
        return SequencingRun.objects.order_by('imported')

class SampleSheetList(generic.ListView):
    template_name = 'lims/samplesheets_list.html'
    context_object_name = 'samplesheets'

    def get_queryset(self):
        """Return the last five samplesheets """
        return SequencingSampleSheet.objects.order_by('imported')

class SamplesList(generic.ListView):
    template_name = 'lims/samples_list.html'
    context_object_name = 'samples'

    def get_queryset(self):
        """Return the last five samples """
        return SequencingSample.objects.order_by('imported')

class SampleDetail(generic.DetailView):
    pk_url_kwarg = 'id'
    model = SequencingSample
    context_object_name = 'sample'
    template_name = 'lims/sample_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['data'] = model_to_dict(context['sample'])
        return context

class RunDetail(generic.DetailView):
    pk_url_kwarg = 'id'
    model = SequencingRun
    context_object_name = 'run'
    template_name = 'lims/run_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['data'] = model_to_dict(context['run'])
        return context

class SampleSheetDetail(generic.DetailView):
    pk_url_kwarg = 'id'
    model = SequencingSampleSheet
    context_object_name = 'samplesheet'
    template_name = 'lims/samplesheet_detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['data'] = model_to_dict(context['samplesheet'])
        return context
