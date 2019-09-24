#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Importation of experiments, runs, samples, etc. for the app database
"""
import os
import sys
# import django
# import datetime
# import csv

# import 'util' and app from top level directory
# intialize Django app to import the
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, parentdir)
# from util import find, samplesheet
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tuco.settings")
# django.setup()
from lims.models import Experiment, Sample, Samplesheet
sys.path.pop(0)

# def import_Sample(sample, runID):
#     """
#     """
#     instance, created = Sample.objects.get_or_create(
#         sample = sample,
#         run_id =  runID,
#         )
#     return(instance, created)

# def import_NGS580sample(sample, sample_data, runID, sheet):
#     """
#     """
#     instance, created = NGS580Sample.objects.get_or_create(
#         run_id = runID,
#         sample = sample,
#         sample_name = sample_data.get('Sample_Name',''),
#         i7_index = sample_data.get('I7_Index_ID',''),
#         index = sample_data.get('index',''),
#         sample_project = sample_data.get('Sample_Project',''),
#         description = sample_data.get('Description',''),
#         genome_folder = sample_data.get('GenomeFolder',''),
#         samplesheet = sheet)
#     return(instance, created)

# def import_Samples(samples_data, experiment, sheet = None):
#     """
#     """
#     for sample in samples_data:
#         instance, created = import_Sample(sample = sample.get('Sample_ID'), runID = experiment)

# def import_NGS580samples(samples_data, experiment, sheet = None):
#     """
#     """


# def import_NGS580samplesheet(sheet, runID):
#     """
#     """
#     instance, created = NGS580SampleSheet.objects.get_or_create(
#         run_id =  runID,
#         path = sheet.path,
#         md5 = sheet.md5
#         )
#     return(instance, created)

# def import_NGS580samplesheets(samplesheets):
#     """
#     """
#     all_created = []
#     not_created = []
#     for sheet in samplesheets:
#         # load the custom samplesheet object from the file
#         sheet_obj = samplesheet.IEMFile(path = sheet)
#         # get runID from the parent directory name
#         runID = os.path.basename(os.path.dirname(sheet))
#         # check for an associated samples pairs file in the same location
#         pairs_sheet = os.path.join(os.path.dirname(sheet), 'samples.pairs.csv')
#         # look up the associated Experiment
#         experiment_instance = Experiment.objects.get(run_id = runID)
#
#         import_Samples(samples_data = sheet_obj.data['Data']['Samples'], experiment = experiment_instance)
        # import_NGS580samples(samples_data = sheet_obj.data['Data']['Samples'], experiment = experiment)
        #
        #
        # # import the base Sample entries
        # for sample in sheet_obj.data['Data']['Samples']:
        #     instance, created = import_Sample(sample = sample.get('Sample_ID'), runID = experiment)
        #
        # # make sure its an NGS580 experiment
        # if experiment.type == 'NGS580':
        #     # get the NGS580 instance from the database
        #     ngs580experiment_instance = NGS580Experiment.objects.get(run_id = experiment)
        #     # import the samplesheet object into the database
        #     instance, created = import_NGS580samplesheet(sheet = sheet_obj, runID = ngs580experiment_instance)
        #     if created:
        #         all_created.append((instance, created))
        #     if not created:
        #         not_created.append((instance, created))
        #     # try to import the samples from the sheet
        #     sheet_instance = NGS580SampleSheet.objects.get(md5 = sheet_obj.md5)
        #     for sample in sheet_obj.data['Data']['Samples']:
        #         sample_instance = Sample.objects.get(
        #             run_id = experiment,
        #             sample = sample.get('Sample_ID')
        #             )
        #         import_NGS580sample(sample = sample_instance, sample_data = sample, runID = ngs580experiment_instance, sheet = sheet_instance)
        #
        #     # check if there were paired samples in the run
        #     # check if the samplesheet file contained info for the pairs
        #     for sample in sheet_obj.data['Data']['Samples']:
        #         if sample.get('Paired_Normal', None):
        #             # get the sample instance
        #             sample_instance = NGS580Sample.objects.get(
        #                 run_id = ngs580experiment_instance,
        #                 samplesheet = sheet_instance,
        #                 sample = sample.get('Sample_ID')
        #                 )
        #             # check if it already has a Normal sample
        #             if sample_instance.paired_normal and sample_instance.paired_normal != '':
        #                 # dont need to do anything
        #                 continue
        #             else:
        #                 # get the paired sample instance
        #                 paired_normal = NGS580Sample.objects.get(
        #                     run_id = ngs580experiment_instance,
        #                     samplesheet = sheet_instance,
        #                     sample = sample.get('Paired_Normal')
        #                     )
        #                 # update the sample with the pair
        #                 sample_instance.paired_normal = paired_normal
        #                 sample_instance.save(update_fields=['paired_normal'])
        #
        #     # check if samples.pairs.csv exists for import
        #     if os.path.exists(pairs_sheet):
        #         pairs = {}
        #         with open(pairs_sheet) as f:
        #             reader = csv.DictReader(f)
        #             for row in reader:
        #                 pairs[row['#SAMPLE-T']] = row['#SAMPLE-N']
        #         # update the samples with the pairs info
        #         for sample in sheet_obj.data['Data']['Samples']:
        #             Sample_ID = sample.get('Sample_ID')
        #             # make sure the sample ID is in the pairs sheet
        #             if Sample_ID in pairs:
        #                 # sample has a pair listed in samples.pairs.csv
        #                 if pairs[Sample_ID] != 'NA':
        #                     paired_sample_ID = pairs[Sample_ID]
        #                     # get the sample instance
        #                     sample_instance = NGS580Sample.objects.get(
        #                         run_id = ngs580experiment_instance,
        #                         samplesheet = sheet_instance,
        #                         sample = Sample_ID
        #                         )
        #                     # get the paired sample instance
        #                     paired_normal = NGS580Sample.objects.get(
        #                         run_id = ngs580experiment_instance,
        #                         samplesheet = sheet_instance,
        #                         sample = paired_sample_ID
        #                         )
        #                     sample_instance.paired_normal = paired_normal
        #                     sample_instance.save(update_fields=['paired_normal'])
    # return(all_created, not_created)

# def import_NGS580experiment(runID, dir):
#     """
#     """
#     experiment = Experiment.objects.get(run_id = runID)
#     parts = runID.split('_')
#     # check if runID can be parsed
#     if len(parts) == 4: # ['180711', 'NB501073', '0057', 'AHFLL2BGX7']
#         run_date = datetime.datetime.strptime(parts[0], '%y%m%d')
#         instrument = parts[1]
#         run_num = parts[2]
#         flowcell = parts[3]
#
#         # import to db
#         NGS580Experiment.objects.get_or_create(
#             run_id = experiment,
#             path = dir,
#             run_date = run_date,
#             instrument = instrument,
#             run_num = run_num,
#             flowcell = flowcell
#             )
#     else:
#         NGS580Experiment.objects.get_or_create(
#             run_id = experiment,
#             path = dir
#             )

# def import_experiment(runID):
#     """
#     Creates an experiment entry in the database
#     """
#     instance, created = Experiment.objects.get_or_create(
#     run_id = runID
#     )
#     return(instance, created)
#
# def import_experiments(runIDs):
#     """
#     Creates multiple experiment entries in the database
#     """
#     all_created = []
#     not_created = []
#     for runID in runIDs:
#         instance, created = import_experiment(runID = runID)
#         if created:
#             all_created.append((instance, created))
#         if not created:
#             not_created.append((instance, created))
#     return(all_created, not_created)
#
# def update_experiment_type(runID, type):
#     """
#     Updates an experiment's missing or empty 'type' value
#     """
#     # get the entry from database
#     instance = Experiment.objects.get(run_id = runID)
#     # check if it already has type
#     if not instance.type or instance.type == '' and type != '' and type is not None:
#         instance.type = type
#         instance.save(update_fields=['type'])
#
# def import_experiments_dir(dir):
#     """
#     Imports Experiments from subdirectories in the provided location
#     """
#     # find experiment run directories
#     importDirs = find.find(search_dir = dir, search_type = 'dir', exclusion_patterns = ['.*'], level_limit = 0)
#     # try to import the experiments
#     all_created, not_created = import_experiments(runIDs = [ os.path.basename(x) for x in importDirs ])
#     # check for exptype files to update with
#     for importDir in importDirs:
#         exptype_file = os.path.join(importDir, 'exptype.txt')
#         exptype = None
#         # read the experiment type from the file and update
#         if os.path.exists(exptype_file):
#             with open(exptype_file) as f:
#                 lines = f.readlines()
#                 exptype = lines[0].strip()
#             update_experiment_type(runID = os.path.basename(importDir), type = exptype)
#         # if exptype == 'NGS580':
#         #     import_NGS580experiment(runID = os.path.basename(importDir), dir = os.path.realpath(importDir))
#
# def import_samplesheets(samplesheets):
#     all_created = []
#     not_created = []
#     for sheet in samplesheets:
#         # load the custom samplesheet object from the file
#         sheet_obj = samplesheet.IEMFile(path = sheet)
#         # get runID from the parent directory name
#         runID = os.path.basename(os.path.dirname(sheet))
#         # look up the associated Experiment
#         experiment_instance = Experiment.objects.get(run_id = runID)
#         import_samplesheet(sheet = sheet_obj, runID = experiment_instance)
#
# def import_samplesheet(sheet, runID):
#     """
#     """
#     print(runID)
#     instance, created = Samplesheet.objects.get_or_create(
#         run_id =  runID,
#         path = sheet.path,
#         md5 = sheet.md5
#         )
#     return(instance, created)
#
#
# def import_samplesheets_dir(dir):
#     #  find all the samplesheets in the dir
#     samplesheets = find.find(search_dir = dir, inclusion_patterns = ['SampleSheet.csv'], level_limit = 1)
#     import_samplesheets(samplesheets = samplesheets)
#
#
# def import_NGS580samplesheets_dir(dir):
#     """
#     Imports all NGS580 samplesheets from the supplied directory
#     """
#     import_samplesheets_dir(dir)
#     #  find all the samplesheets in the dir
#     samplesheets = find.find(search_dir = dir, inclusion_patterns = ['SampleSheet.csv'], level_limit = 1)
#     # import_NGS580samplesheets(samplesheets = samplesheets)


if __name__ == '__main__':
    pass
    # file or directory to import from
    # inputItem = os.path.realpath(sys.argv[1])
    # type of thing to import from that location
    # inputType = sys.argv[2]

    # if inputType == 'exps':
    #     import_experiments_dir(dir = inputItem)
    # elif inputType == 'NGS580samplesheets':
    #     import_NGS580samplesheets_dir(dir = inputItem)
    # else:
    #     print('ERROR: did not recognize input type arg')
