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
from lims.models import SequencingSampleSheet


sheets_dir = os.path.realpath(sys.argv[1])

#  find all the samplesheets in the dir
for sheet_file in find.find(search_dir = sheets_dir, inclusion_patterns = ['SampleSheet.csv']):
    sheet = samplesheet.IEMFile(path = os.path.realpath(sheet_file))
    seqtype_file = os.path.join(os.path.dirname(sheet_file), 'seqtype.txt')
    Run_ID = os.path.basename(os.path.dirname(sheet_file))

    # load seqtype
    if os.path.exists(seqtype_file):
        with open(seqtype_file) as f:
            lines = f.readlines()
            Seq_Type = lines[0].strip()

            # get the samplesheet entry from database
            sheet_instance = SequencingSampleSheet.objects.get(md5 = sheet.meta['Sheet_md5'])

            # check if it already has seq_type..
            if not sheet_instance.seq_type or sheet_instance.seq_type == '' and Seq_Type != '':
                sheet_instance.seq_type = Seq_Type
                sheet_instance.save(update_fields=['seq_type'])
            # else:
            #     print('>>> seqtype already listed as: {0}'.format(sheet_instance.seq_type))
