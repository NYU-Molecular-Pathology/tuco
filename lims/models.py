from django.db import models
import hashlib

class SequencingSample(models.Model):
    """
    Database model for a sample that was submitted for DNA sequencing, based on the
    data provided in a standard bcl2fastq IEM formatted SampleSheet.csv file
    """
    Run_ID = models.ForeignKey('SequencingRun', blank=True, null=True, on_delete=models.SET_NULL)
    Sample_ID = models.TextField()
    Sample_Name = models.TextField(blank=True)
    Paired_Normal = models.TextField(blank=True)
    I7_Index_ID = models.TextField(blank=True)
    index = models.TextField(blank=True)
    Sample_Project = models.TextField(blank=True)
    Description = models.TextField(blank=True)
    GenomeFolder = models.TextField(blank=True)
    IEMFileVersion = models.TextField(blank=True)
    Investigator_Name = models.TextField(blank=True) # Investigator Name
    Project_Name = models.TextField(blank=True) # Project Name
    Experiment_Name = models.TextField(blank=True) # Experiment Name
    Date = models.TextField(blank=True)
    Workflow = models.TextField(blank=True)
    Application = models.TextField(blank=True)
    Assay = models.TextField(blank=True)
    Chemistry = models.TextField(blank=True)
    AdapterSequenceRead1 = models.TextField(blank=True)
    AdapterSequenceRead2 = models.TextField(blank=True)
    Sheet_path = models.TextField(blank=True)
    Sheet_md5 = models.TextField(blank=True)
    Sheet_host = models.TextField(blank=True)
    hash = models.TextField(blank = True, unique = True)

    def save(self, *args, **kwargs):
        # update the 'hash' field based on the essential entry attributes
        d = {
        'Run_ID' : self.Run_ID.Run_ID,
        'Sample_ID' : self.Sample_ID,
        'Sample_Name' : self.Sample_Name,
        'Paired_Normal' : self.Paired_Normal,
        'Sheet_md5' : self.Sheet_md5
        }
        try:
            # python 2.x
            md5 = hashlib.md5( str(''.join(d.values())) ).hexdigest()
        except:
            # python 3.x
            md5 = hashlib.md5( str(''.join(d.values())).encode('utf-8') ).hexdigest()
        self.hash = md5
        super().save(*args, **kwargs)

    def __str__(self):
        return self.Sample_ID

class SequencingSampleSheet(models.Model):
    """
    Database model for an IEM formatted SampleSheet.csv file, used for demultiplexing with bcl2fastq
    """
    Run_ID = models.TextField(blank = True)
    Sheet_path = models.TextField(blank = True)
    Sheet_md5 = models.TextField(blank=True, unique = True)
    Sheet_host = models.TextField(blank=True)
    hash = models.TextField(blank = True)

    def save(self, *args, **kwargs):
        # update the 'hash' field with the entry attributes
        d = {
        'Run_ID' : self.Run_ID.Run_ID, # get the string here !!
        'Sheet_path': self.Sheet_path,
        'Sheet_md5' : self.Sheet_md5,
        'Sheet_host' : self.Sheet_host
        }
        try:
            # python 2.x
            md5 = hashlib.md5( str(''.join(d.values())) ).hexdigest()
        except:
            # python 3.x
            md5 = hashlib.md5( str(''.join(d.values())).encode('utf-8') ).hexdigest()
        self.hash = md5
        super().save(*args, **kwargs)

    def __str__(self):
        msg = '{0} [{1}]'.format(self.Run_ID, self.hash[0:6])
        return msg

class SequencingRun(models.Model):
    """
    Database model for a sequencing run, as output by the sequencer
    """
    Run_ID = models.TextField(unique = True)
    Run_path = models.TextField(blank=True)
    Sheet_path = models.TextField(blank=True)
    Sheet_md5 = models.TextField(blank=True)
    Sheet_host = models.TextField(blank=True)
    Seq_Type = models.TextField(blank=True)
    Sequencer_Serial = models.TextField(blank=True)
    Run_Num = models.TextField(blank=True)
    Flowcell_ID = models.TextField(blank=True)
    Date = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.Run_ID
