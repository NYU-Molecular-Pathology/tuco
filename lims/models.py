import os
import hashlib
import datetime
from django.db import models
from django.core.files import File
from django.utils.timezone import now
# RUNS_DIR = os.path.realpath(os.environ['RUNS'])

experiment_types = (
('FUSION-SEQer', 'FUSION-SEQer'), # Archer
('NGS580', 'NGS580'),
('NGS629', 'NGS629')
)
class Experiment(models.Model):
    """
    An experiment conducted by the wet lab
    Example: sequencing runs, methylation array, etc.
    """
    experiment_id = models.CharField(verbose_name = 'Experiment ID (Run ID)', max_length=255) # unique = True,
    type = models.CharField(choices = experiment_types, max_length=255, blank = False, null = False)
    imported = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)

    def save(self, *args, **kwargs):
        # make sure that only entries with valid experiment types can be saved
        if self.type in [i[0] for i in experiment_types]:
          super().save(*args, **kwargs)
        else:
            raise Exception("Experiment.type takes only the following: {0}".format([i[0] for i in experiment_types]))

    def __str__(self):
        return "[{0}] {1}".format(self.type, self.experiment_id)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['experiment_id','type'], name = 'unique_experiment_id_type'),
            ]

class Sample(models.Model):
    """
    A unique physical sample processed by the wet lab
    """
    sample_id = models.CharField(max_length = 255, verbose_name = 'Sample ID', unique = True, blank = False, null = False)
    imported = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0}".format(self.sample_id)

class SampleExperiment(models.Model):
    """
    A listing for a specific sample's usage in a specific experiment
    """
    sample = models.ForeignKey('Sample', blank=False, null=False, on_delete = models.CASCADE)
    experiment = models.ForeignKey('Experiment', blank=False, null=False, on_delete = models.CASCADE)
    imported = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "[{0} : {1}] {2}".format(
            self.experiment.type[:6],
            self.experiment.experiment_id,
            self.sample.sample_id)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields = ['experiment','sample'], name = 'unique_experiment_id_type'),
            ]

# SAMPLESHEETS_EXTERNAL_DIR = os.path.realpath(os.environ['SAMPLESHEETS_EXTERNAL_DIR'])
def samplesheet_upload_path(instance, filename):
    """
    user uploaded samplesheet file will be uploaded to MEDIA_ROOT/<experiment_type>/<experiment_id>/<filename>
    """
    # p = '{0}/{1}/{2}/{3}'.format(...) datetime.datetime.strftime(now(), '%Y-%m-%d'),
    p = os.path.join(
        instance.experiment.type,
        instance.experiment.experiment_id,
        os.path.basename(filename)
    )
    return(p)

class Samplesheet(models.Model):
    experiment = models.OneToOneField(Experiment, on_delete=models.CASCADE)
    # user uploaded sheet file
    file = models.FileField(upload_to = samplesheet_upload_path)
    imported = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{0}".format(self.file)
    # path to externally imported samplesheet file
    # external_path = models.FilePathField(path = SAMPLESHEETS_EXTERNAL_DIR, blank = True, recursive = True, match = 'SampleSheet.csv')
#     run_id = models.ForeignKey('Experiment', blank=True, null=True, db_column = 'run_id', on_delete = models.CASCADE)
#     type = models.CharField(choices=experiment_types, max_length=10)
#     md5 = models.TextField(blank=True, unique = True) # file identifier
#     hash = models.TextField(blank = True) # db entry identifier
#
#     def save(self, *args, **kwargs):
#         """
#         update the 'hash' field with the entry attributes
#         to ensure a unique, recognizable ID for each entry
#         """
#         # update the 'type' from the Experiment
#         type = self.run_id.type
#         self.type = type
#
#         # update the hash
#         d = {
#         'run_id' : self.run_id.run_id, # get the string here !!
#         'path': self.path,
#         'md5' : self.md5
#         }
#         try:
#             # python 2.x
#             md5 = hashlib.md5( str(''.join(d.values())) ).hexdigest()
#         except:
#             # python 3.x
#             md5 = hashlib.md5( str(''.join(d.values())).encode('utf-8') ).hexdigest()
#         self.hash = md5
#
#         # if a path exists but an upload file does not, save the path into the file
#         if not self.file and self.path:
#             # with open(self.path, 'rb') as f:
#             f = open(self.path, 'rb')
#             self.file = File(f)
#
#         # call the parent save method
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         msg = '{0} [{1}]'.format(self.run_id, self.hash[0:6])
#         return msg

#
# class NGS580Sample(models.Model):
#     """
#     Database model for a sample that was submitted for DNA sequencing, based on the
#     data provided in a standard bcl2fastq IEM formatted SampleSheet.csv file
#     """
#     run_id = models.ForeignKey('NGS580Experiment', blank=True, null=True, db_column = 'run_id', on_delete = models.CASCADE) # on_delete=models.SET_NULL
#     sample = models.ForeignKey('Sample', blank=False, null=False, db_column = 'sample_id', on_delete = models.CASCADE) # on_delete=models.SET_NULL
#     # attributes from SampleSheet.csv
#     sample_name = models.TextField(blank=True, verbose_name = 'Sample_Name')
#     # sample_id of a paired 'normal' sample
#     paired_normal = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
#     i7_index = models.TextField(blank=True, verbose_name = 'I7_Index_ID')
#     index = models.TextField(blank=True)
#     sample_project = models.TextField(blank=True, verbose_name = 'Sample_Project')
#     description = models.TextField(blank=True, verbose_name = 'Description')
#     genome_folder = models.TextField(blank=True, verbose_name = 'GenomeFolder')
#     samplesheet = models.ForeignKey('NGS580SampleSheet', blank=True, null=True, on_delete=models.SET_NULL)
#     imported = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.sample
#
# class NGS580SampleSheet(models.Model):
#     """
#     Database model for an IEM formatted SampleSheet.csv file, used for demultiplexing with bcl2fastq
#     """
#     # _id appended to db column by default on foreign keys...
#     run_id = models.ForeignKey('NGS580Experiment', blank=True, null=True, db_column = 'run_id', on_delete = models.CASCADE) # on_delete=models.SET_NULL
#     sheet = models.ForeignKey('Samplesheet', blank=False, null=False, on_delete = models.CASCADE) #
#     # path to externally imported samplesheet file
#     path = models.FilePathField(path = SAMPLESHEETS_DIR, blank = True, recursive = True, match = 'SampleSheet.csv')
#     # user uploaded sheet file
#     file = models.FileField(upload_to = samplesheet_upload_path)
#     md5 = models.TextField(blank=True, unique = True)
#
#     # optional fields from the original samplesheet
#     iem_file_version = models.TextField(blank=True, verbose_name = 'IEMFileVersion')
#     investigator_name = models.TextField(blank=True, verbose_name = 'Investigator Name')
#     project_name = models.TextField(blank=True, verbose_name = 'Project Name')
#     experiment_name = models.TextField(blank=True, verbose_name = 'Experiment Name')
#     date = models.TextField(blank=True, verbose_name = 'Date')
#     workflow = models.TextField(blank=True, verbose_name = 'Workflow')
#     application = models.TextField(blank=True, verbose_name = 'Application')
#     assay = models.TextField(blank=True, verbose_name = 'Assay')
#     chemistry = models.TextField(blank=True, verbose_name = 'Chemistry')
#     adapter_sequence_read_1 = models.TextField(blank=True, verbose_name = 'AdapterSequenceRead1')
#     adapter_sequence_read_2 = models.TextField(blank=True, verbose_name = 'AdapterSequenceRead2')
#     hash = models.TextField(blank = True)
#     imported = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#
#     def save(self, *args, **kwargs):
#         """
#         update the 'hash' field with the entry attributes
#         to ensure a unique, recognizable ID for each entry
#         """
#         # update the hash
#         d = {
#         'run_id' : self.run_id.run_id.run_id, # get the string here !!
#         'path': self.path,
#         'md5' : self.md5
#         }
#         try:
#             # python 2.x
#             md5 = hashlib.md5( str(''.join(d.values())) ).hexdigest()
#         except:
#             # python 3.x
#             md5 = hashlib.md5( str(''.join(d.values())).encode('utf-8') ).hexdigest()
#         self.hash = md5
#
#         # if a path exists but an upload file does not, save the path into the file
#         if not self.file and self.path:
#             # with open(self.path, 'rb') as f:
#             f = open(self.path, 'rb')
#             self.file = File(f)
#
#         # call the parent save method
#         super().save(*args, **kwargs)
#
#     def __str__(self):
#         msg = '{0} [{1}]'.format(self.run_id, self.hash[0:6])
#         return msg
#
# class NGS580Experiment(models.Model):
#     """
#     Database model for a sequencing run, as output by the sequencer
#     """
#     # run_id = models.TextField(unique = True, verbose_name = 'Run ID')
#     run_id = models.ForeignKey('Experiment', blank=True, null=True, db_column = 'run_id', on_delete = models.CASCADE) # on_delete=models.SET_NULL
#     # path to directory where instrument outputs data for run
#     path = models.FilePathField(blank=True, path = RUNS_DIR, recursive = False, allow_files = False, allow_folders = True)
#     instrument = models.TextField(blank=True)
#     run_num = models.TextField(blank=True)
#     flowcell = models.TextField(blank=True)
#     run_date = models.DateField(blank=True, null=True)
#     imported = models.DateTimeField(auto_now_add=True)
#     updated = models.DateTimeField(auto_now=True)
#
#     def __str__(self):
#         return self.run_id.__str__()
