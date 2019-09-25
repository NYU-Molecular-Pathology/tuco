from django.contrib import admin

from .models import Experiment
from .models import Sample
from .models import Samplesheet

admin.site.register(Experiment)
admin.site.register(Sample)
admin.site.register(Samplesheet)
