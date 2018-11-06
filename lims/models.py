import os
import hashlib
import datetime
from django.db import models
from django.core.files import File
from django.utils.timezone import now

SAMPLESHEETS_DIR = os.path.realpath(os.environ['SAMPLESHEETS'])
RUNS_DIR = os.path.realpath(os.environ['RUNS'])

class SequencingSample(models.Model):
    """
    Database model for a sample that was submitted for DNA sequencing, based on the
    data provided in a standard bcl2fastq IEM formatted SampleSheet.csv file
    """
    run_id = models.ForeignKey('SequencingRun', blank=True, null=True, on_delete=models.SET_NULL, db_column = 'run_id')
    sample = models.TextField(verbose_name = 'Sample ID')
    # attributes from SampleSheet.csv
    sample_name = models.TextField(blank=True, verbose_name = 'Sample_Name')
    # sample_id of a paired 'normal' sample
    paired_normal = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    i7_index = models.TextField(blank=True, verbose_name = 'I7_Index_ID')
    index = models.TextField(blank=True)
    sample_project = models.TextField(blank=True, verbose_name = 'Sample_Project')
    description = models.TextField(blank=True, verbose_name = 'Description')
    genome_folder = models.TextField(blank=True, verbose_name = 'GenomeFolder')
    samplesheet = models.ForeignKey('SequencingSampleSheet', blank=True, null=True, on_delete=models.SET_NULL)
    imported = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.sample


def samplesheet_upload_path(instance, filename):
    """
    user uploaded samplesheet file will be uploaded to MEDIA_ROOT/<date>/<run_id>/<filename>
    """
    p = '{0}/{1}/{2}'.format(
    datetime.datetime.strftime(now(), '%Y-%m-%d'),
    instance.run_id.run_id,
    os.path.basename(filename)
    )
    return(p)


class SequencingSampleSheet(models.Model):
    """
    Database model for an IEM formatted SampleSheet.csv file, used for demultiplexing with bcl2fastq
    """
    # _id appended to db column by default on foreign keys...
    run_id = models.ForeignKey('SequencingRun', blank=True, null=True, on_delete=models.SET_NULL, db_column = 'run_id')
    # path to externally imported samplesheet file
    path = models.FilePathField(path = SAMPLESHEETS_DIR, blank = True, recursive = True, match = 'SampleSheet.csv')
    # user uploaded sheet file
    file = models.FileField(upload_to = samplesheet_upload_path)
    md5 = models.TextField(blank=True, unique = True)
    host = models.TextField(blank=True)

    seq_types = (
    ('Archer', 'Archer'),
    ('NGS580', 'NGS580')
    )
    seq_type = models.CharField(choices=seq_types, max_length=10)  # default='ngs580'

    # optional fields from the original samplesheet
    iem_file_version = models.TextField(blank=True, verbose_name = 'IEMFileVersion')
    investigator_name = models.TextField(blank=True, verbose_name = 'Investigator Name')
    project_name = models.TextField(blank=True, verbose_name = 'Project Name')
    experiment_name = models.TextField(blank=True, verbose_name = 'Experiment Name')
    date = models.TextField(blank=True, verbose_name = 'Date')
    workflow = models.TextField(blank=True, verbose_name = 'Workflow')
    application = models.TextField(blank=True, verbose_name = 'Application')
    assay = models.TextField(blank=True, verbose_name = 'Assay')
    chemistry = models.TextField(blank=True, verbose_name = 'Chemistry')
    adapter_sequence_read_1 = models.TextField(blank=True, verbose_name = 'AdapterSequenceRead1')
    adapter_sequence_read_2 = models.TextField(blank=True, verbose_name = 'AdapterSequenceRead2')
    hash = models.TextField(blank = True)
    imported = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        update the 'hash' field with the entry attributes
        to ensure a unique, recognizable ID for each entry
        """
        # update the hash
        d = {
        'run_id' : self.run_id.run_id, # get the string here !!
        'path': self.path,
        'md5' : self.md5,
        'host' : self.host
        }
        try:
            # python 2.x
            md5 = hashlib.md5( str(''.join(d.values())) ).hexdigest()
        except:
            # python 3.x
            md5 = hashlib.md5( str(''.join(d.values())).encode('utf-8') ).hexdigest()
        self.hash = md5

        # if a path exists but an upload file does not, save the path into the file
        if not self.file and self.path:
            # with open(self.path, 'rb') as f:
            f = open(self.path, 'rb')
            self.file = File(f)

        # call the parent save method
        super().save(*args, **kwargs)

    def __str__(self):
        msg = '{0} [{1}]'.format(self.run_id, self.hash[0:6])
        return msg

class SequencingRun(models.Model):
    """
    Database model for a sequencing run, as output by the sequencer
    """
    run_id = models.TextField(unique = True, verbose_name = 'Run ID')
    # path to directory where instrument outputs data for run
    path = models.FilePathField(blank=True, path = RUNS_DIR, recursive = False, allow_files = False, allow_folders = True)
    device_serial = models.TextField(blank=True)
    run_num = models.TextField(blank=True)
    flowcell = models.TextField(blank=True)
    run_date = models.DateField(blank=True, null=True)
    imported = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.run_id
