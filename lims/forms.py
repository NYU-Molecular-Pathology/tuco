from django import forms
from .models import SequencingSampleSheet, SequencingRun

class SequencingSampleSheetForm(forms.ModelForm):
    samplesheet = forms.FileField()

    class Meta:
        model = SequencingSampleSheet
        fields = ('run_id', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['run_id'].queryset = SequencingRun.objects.values_list('run_id', flat=True).distinct()
        self.fields['run_id'].required = True
