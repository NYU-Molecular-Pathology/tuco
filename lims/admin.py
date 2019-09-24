from django.contrib import admin

from .models import Experiment
from .models import Sample
from .models import ExperimentSample
from .models import Samplesheet
from .models import SamplesheetSample

admin.site.register(Experiment)
admin.site.register(Sample)
admin.site.register(ExperimentSample)
admin.site.register(Samplesheet)
admin.site.register(SamplesheetSample)
