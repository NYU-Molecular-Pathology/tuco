#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Imports all samplesheets in a directory into the database

Directory structure should be like this:
$ tree samplesheets
samplesheets
|-- 170512_NB501073_0009_AHF5H2BGX2
|   |-- SampleSheet.csv
|   |-- seqtype.txt
|   `-- samples.pairs.csv
|-- 170519_NB501073_0010_AHCLLMBGX2
|   |-- SampleSheet.csv
|   |-- seqtype.txt
|   `-- samples.pairs.csv
|-- 170526_NB501073_0011_AHCJTYBGX2
|   |-- SampleSheet.csv
|   |-- seqtype.txt
|   `-- samples.pairs.csv
...
...
etc.

SampleSheet.csv: bcl2fastq samplesheet
samples.pairs.csv: Tumor - Normal pairs sheet, formatted like this:
seqtype.txt: label for the type of sequencing (NGS580 or Archer)
directory name: runID from the sequencer

$ cat samplesheets/180112_NB501073_0029_AHT5KFBGX3/samples.pairs.csv
#SAMPLE-T,#SAMPLE-N
Tumor1,Normal1
Tumor2,Normal2
Tumor3,Normal3


$ cat seqtype.txt
Archer

run with this:

$ python import-samplesheets.py samplesheets/
"""
import os
import sys
import csv
import getpass
from util import samplesheet
from util import find
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tuco.settings")
import django
django.setup()
from lims.models import SequencingSample, SequencingRun, SequencingSampleSheet


sheets_dir = sys.argv[1]

#  find all the samplesheets in the dir
for sheet_file in find.find(search_dir = sheets_dir, inclusion_patterns = ['SampleSheet.csv']):
    sheet = samplesheet.IEMFile(path = sheet_file)
    Run_ID = os.path.basename(os.path.dirname(sheet_file))
    pairs_sheet = os.path.join(os.path.dirname(sheet_file), 'samples.pairs.csv')
    pairs = False

    # check if a pairs sheet exists; if so, import it and
    if os.path.exists(pairs_sheet):
        pairs = {}
        with open(pairs_sheet) as f:
            reader = csv.DictReader(f)
            for row in reader:
                pairs[row['#SAMPLE-T']] = row['#SAMPLE-N']

    # update each record and add to database
    for record in sheet.flatten():
        # register the SampleSheet in the database if its not there already
        SequencingSampleSheet.objects.get_or_create(
        Run_ID =  SequencingRun.objects.get(Run_ID = Run_ID),
        Sheet_external_path = record.get('Sheet_path',''),
        Sheet_md5 = record.get('Sheet_md5',''),
        Sheet_host = record.get('Sheet_host','')
        )

        Sample_Name = record.get('Sample_Name')
        Paired_Normal = record.get('Paired_Normal','NONE')

        # check for a pair
        if Paired_Normal == 'NONE': # Pair not already in SampleSheet.csv
            if pairs is not False: # samples.pairs.csv file was imported
                if Sample_Name in pairs: # sample is in samples.pairs.csv
                    if pairs[Sample_Name] != 'NA': # sample has a pair listed in samples.pairs.csv
                        record['Paired_Normal'] = pairs[Sample_Name]

        # add to db # get_or_create
        SequencingSample.objects.get_or_create(
            Run_ID = SequencingRun.objects.get(Run_ID = Run_ID),
            Sample_ID = record.get('Sample_ID',''),
            Sample_Name = record.get('Sample_Name',''),
            Paired_Normal = record.get('Paired_Normal',''),
            I7_Index_ID = record.get('I7_Index_ID',''),
            index = record.get('index',''),
            Sample_Project = record.get('Sample_Project',''),
            Description = record.get('Description',''),
            GenomeFolder = record.get('GenomeFolder',''),
            IEMFileVersion = record.get('IEMFileVersion',''),
            Investigator_Name = record.get('Investigator_Name',''), # Investigator Name
            Project_Name = record.get('Project_Name',''), # Project Name
            Experiment_Name = record.get('Experiment_Name',''), # Experiment Name
            Date = record.get('Date',''),
            Workflow = record.get('Workflow',''),
            Application = record.get('Application',''),
            Assay = record.get('Assay',''),
            Chemistry = record.get('Chemistry',''),
            AdapterSequenceRead1 = record.get('AdapterSequenceRead1',''),
            AdapterSequenceRead2 = record.get('AdapterSequenceRead2',''),
            Sheet_path = record.get('Sheet_path',''),
            Sheet_md5 = record.get('Sheet_md5',''),
            Sheet_host = record.get('Sheet_host','')
        )
