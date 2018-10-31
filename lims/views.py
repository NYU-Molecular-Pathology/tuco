from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("This is the LIMS index.")

def runs(request):
    return HttpResponse("You're looking at all runs.")

def run(request, id):
    return HttpResponse("You're looking at run {0}.".format(id))

def sample(request, id):
    return HttpResponse("You're looking at sample {0}.".format(id))

def samples(request):
    return HttpResponse("You're looking at all samples.")

def samplesheet(request, id):
    return HttpResponse("You're looking at samplesheet {0}.".format(id))

def samplesheets(request):
    return HttpResponse("You're looking at all samplesheets.")
