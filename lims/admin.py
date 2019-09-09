from django.contrib import admin

from .models import Experiment
from .models import Sample
from .models import SampleExperiment
# from .models import NGS580Experiment
# from .models import NGS580SampleSheet
# from .models import NGS580Sample

admin.site.register(Experiment)
admin.site.register(Sample)
admin.site.register(SampleExperiment)
# admin.site.register(NGS580Experiment)
# admin.site.register(NGS580SampleSheet)
# admin.site.register(NGS580Sample)
