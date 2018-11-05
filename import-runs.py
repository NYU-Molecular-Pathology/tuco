#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Imports all runs based on the directory names at the given path

$ ls -1 samplesheets
170308_NB501073_0004_AHHFKYBGX2
170426_NB501073_0008_AHCKY5BGX2
170512_NB501073_0009_AHF5H2BGX2
170519_NB501073_0010_AHCLLMBGX2
170526_NB501073_0011_AHCJTYBGX2
...
...

"""
import os
import sys
import datetime
from util import find
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tuco.settings")
import django
django.setup()
from lims.models import SequencingRun

seq_dir = os.path.realpath(sys.argv[1])

for run_dir in  find.find(search_dir = seq_dir, search_type = 'dir', exclusion_patterns = ['.*'], level_limit = 0):
    Run_ID = os.path.basename(run_dir)
    Run_path = os.path.realpath(run_dir)
    seqtype_file = os.path.join(Run_path, 'seqtype.txt')
    parts = Run_ID.split('_')
    Date = ''
    Sequencer_Serial = ''
    Run_Num = ''
    Flowcell_ID = ''

    # check if Run_ID can be parsed
    if len(parts) == 4: # ['180711', 'NB501073', '0057', 'AHFLL2BGX7']
        Date = datetime.datetime.strptime(parts[0], '%y%m%d')
        Sequencer_Serial = parts[1]
        Run_Num = parts[2]
        Flowcell_ID = parts[3]

        # import to db
        SequencingRun.objects.get_or_create(
            Run_ID = Run_ID,
            Run_path = Run_path,
            Sequencer_Serial = Sequencer_Serial,
            Run_Num = Run_Num,
            Flowcell_ID = Flowcell_ID,
            Date = Date
            )
    else:
        # use empty values instead
        SequencingRun.objects.get_or_create(
            Run_ID = Run_ID,
            Run_path = Run_path,
            Sequencer_Serial = Sequencer_Serial,
            Run_Num = Run_Num,
            Flowcell_ID = Flowcell_ID
            )
