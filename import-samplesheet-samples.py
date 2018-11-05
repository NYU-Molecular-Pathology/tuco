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


sheets_dir = os.path.realpath(sys.argv[1])

#  find all the samplesheets in the dir
for sheet_file in find.find(search_dir = sheets_dir, inclusion_patterns = ['SampleSheet.csv']):
    sheet = samplesheet.IEMFile(path = os.path.realpath(sheet_file))
    Run_ID = os.path.basename(os.path.dirname(sheet_file))
    seqtype_file = os.path.join(os.path.dirname(sheet_file), 'seqtype.txt')
    pairs = False

    # update each record and add to database
    for record in sheet.flatten():
        Sample_Name = record.get('Sample_Name')

        # add to db # get_or_create
        SequencingSample.objects.get_or_create(
            run_id = SequencingRun.objects.get(run_id = Run_ID),
            sample = record.get('Sample_ID',''),
            sample_name = record.get('Sample_Name',''),
            # paired_normal = record.get('Paired_Normal',''), # get this separately!
            i7_index = record.get('I7_Index_ID',''),
            index = record.get('index',''),
            sample_project = record.get('Sample_Project',''),
            description = record.get('Description',''),
            genome_folder = record.get('GenomeFolder',''),
            samplesheet = SequencingSampleSheet.objects.get(md5 = record.get('Sheet_md5'))
        )
