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
from util import samplesheet
from util import find
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tuco.settings")
import django
django.setup()
from lims.models import SequencingRun, SequencingSampleSheet

sheets_dir = os.path.realpath(sys.argv[1])

#  find all the samplesheets in the dir
for sheet_file in find.find(search_dir = sheets_dir, inclusion_patterns = ['SampleSheet.csv']):
    sheet = samplesheet.IEMFile(path = sheet_file)
    Run_ID = os.path.basename(os.path.dirname(sheet_file))
    seqtype_file = os.path.join(os.path.dirname(sheet_file), 'seqtype.txt')

    # register the SampleSheet in the database if its not there already
    SequencingSampleSheet.objects.get_or_create(
    run_id =  SequencingRun.objects.get(run_id = Run_ID),
    path = os.path.realpath(sheet.path),
    md5 = sheet.md5,
    host = sheet.meta.get('Sheet_host', '')
    )
    # IEMFileVersion = record.get('IEMFileVersion',''),
    # Investigator_Name = record.get('Investigator_Name',''), # Investigator Name
    # Project_Name = record.get('Project_Name',''), # Project Name
    # Experiment_Name = record.get('Experiment_Name',''), # Experiment Name
    # Date = record.get('Date',''),
    # Workflow = record.get('Workflow',''),
    # Application = record.get('Application',''),
    # Assay = record.get('Assay',''),
    # Chemistry = record.get('Chemistry',''),
    # AdapterSequenceRead1 = record.get('AdapterSequenceRead1',''),
    # AdapterSequenceRead2 = record.get('AdapterSequenceRead2',''),
