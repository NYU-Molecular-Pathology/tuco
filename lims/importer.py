#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Importation of experiments, runs, samples, etc. for the app database
"""
import os
import sys
import json
# import datetime
# import csv

# import 'util' and app from top level directory
# intialize Django app to import the
parentdir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(0, parentdir)
from util import samplesheet # find
# if invoked from command line, need to initialize Django app
if __name__ == '__main__':
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tuco.settings")
    django.setup()
from lims.models import Experiment, Sample, Samplesheet
sys.path.pop(0)

def import_experiment(experiment_id, experiment_type):
    """
    Import an experiment to the database
    """
    instance, created = Experiment.objects.get_or_create(
        experiment_id = experiment_id,
        type =  experiment_type,
        )
    return(instance, created)

def import_experiment_from_json_file(json_file):
    """
    Import an experiment from a JSON file
    """
    with open(json_file) as f:
        data = json.load(f)
    instance, created = import_experiment(experiment_id = data.get('experiment_id'), experiment_type = data.get('type'))
    return(instance, created)

def get_sampleIDs_from_samplesheet(iem_file):
    """
    Get a list of sample IDs from an IEM formatted samplesheet (SampleSheet.csv)
    """
    sheet = samplesheet.IEMFile(path = iem_file)
    sampleIDs = [ s['Sample_ID'] for s in sheet.data['Data']['Samples'] ]
    return(sampleIDs)

def import_sample(sample_id):
    """
    Import a sample into the database
    """
    instance, created = Sample.objects.get_or_create(sample_id = sample_id)
    return(instance, created)

def import_from_samplesheet(iem_file, 
        experiment_id = False, 
        experiment_type = None, 
        detect_experiment_json = False):
    """
    Import all the samples in the samplesheet
    """
    all_imported_samples = []
    all_not_imported_samples = []
    all_samples_added_experiment = []
    all_samples_not_added_experiment = []
    # get the sample IDs from the sheet
    sampleIDs = get_sampleIDs_from_samplesheet(iem_file = iem_file)
    # try to import the experiment
    # # try to find a file experiment.json and get experiment configs from that
    if detect_experiment_json == True:
        experiment_json_file = os.path.join(os.path.dirname(iem_file), "experiment.json")
        with open(experiment_json_file) as f:
            data = json.load(f)
            experiment_id = data.get('experiment_id')
            experiment_type = data.get('type')
    # # check to make sure args are valid
    if not experiment_id:
        print("ERROR: experiment_id was not provided or determined")
        raise # TODO: handle this better
    if not experiment_type:
        print("ERROR: experiment_type was not provided or determined")
        raise # TODO: handle this better
    # # attempt experiment import
    experiment_instance, experiment_created = import_experiment(
        experiment_id = experiment_id, 
        experiment_type = experiment_type
        )
    # try to create each entry in the database
    for sampleID in sampleIDs:
        sample_instance, sample_created = import_sample(sample_id = sampleID)
        # try to add the experiment to each entry
        try:
            sample_instance.experiment.add(experiment_instance)
            all_samples_added_experiment.append(sample_instance)
        except:
            all_samples_not_added_experiment.append(sample_instance)
        if sample_created:
            all_imported_samples.append(sample_instance)
        else:
            all_not_imported_samples.append(sample_instance)
    return((
    all_imported_samples,
    all_not_imported_samples,
    all_samples_added_experiment,
    all_samples_not_added_experiment,
    experiment_created
    ))





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

def main():
    """
    Main control function for script
    """
    import_item = sys.argv[1]
    import_results = import_from_samplesheet(
        iem_file = import_item, 
        detect_experiment_json = True
        )
    for item in import_results: print(item)

if __name__ == '__main__':
    main()
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
