from django.contrib import admin
from .models import SequencingSample
from .models import SequencingRun
from .models import SequencingSampleSheet

admin.site.register(SequencingSample)
admin.site.register(SequencingRun)
admin.site.register(SequencingSampleSheet)
