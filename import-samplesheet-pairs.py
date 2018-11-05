#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Imports sample pair associations from samplesheets
"""
import os
import sys
import csv
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
        Sample_Name = record.get('Sample_Name')

        # get the database entry for the sample and pair
        sample = SequencingSample.objects.get(
        run_id = SequencingRun.objects.get(run_id = Run_ID),
        sample = record.get('Sample_ID'),
        samplesheet = SequencingSampleSheet.objects.get(md5 = record.get('Sheet_md5'))
        )

        # check if it already has a pair listed
        if sample.paired_normal and sample.paired_normal != '':
            # dont need to do anything
            continue
        else:

            # double check for an entry in the samplesheet
            if record.get('Paired_Normal', None):
                paired_sample_name = record.get('Paired_Normal')
                paired_sample = SequencingSample.objects.get(
                run_id = SequencingRun.objects.get(run_id = Run_ID),
                sample = paired_sample_name,
                samplesheet = SequencingSampleSheet.objects.get(md5 = record.get('Sheet_md5'))
                )
                sample.paired_normal = paired_sample
                sample.save(update_fields=['paired_normal'])
                continue

            # samples.pairs.csv file was imported
            if pairs is not False:
                # sample is in samples.pairs.csv
                if Sample_Name in pairs:
                    # sample has a pair listed in samples.pairs.csv
                    if pairs[Sample_Name] != 'NA':
                        paired_sample_name = pairs[Sample_Name]
                        paired_sample = SequencingSample.objects.get(
                        run_id = SequencingRun.objects.get(run_id = Run_ID),
                        sample = paired_sample_name,
                        samplesheet = SequencingSampleSheet.objects.get(md5 = record.get('Sheet_md5'))
                        )
                        sample.paired_normal = paired_sample
                        sample.save(update_fields=['paired_normal'])
                        continue
