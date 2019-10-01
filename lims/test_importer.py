import os
import sys
import json
from django.test import TestCase, override_settings
from .models import Experiment
from .models import Sample
from .models import Samplesheet
import shutil

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_dir)
import importer
sys.path.pop(0)

MEDIA_ROOT_TEST = os.path.realpath(os.environ['MEDIA_ROOT_TEST'])
FIXTURES_DIR = os.path.realpath(os.environ['FIXTURES_DIR'])
TEST_EXPERIMENTS_DIR = os.path.join(FIXTURES_DIR, 'experiments')
TEST_EXPERIMENT_JSON1 = os.path.join(TEST_EXPERIMENTS_DIR, 'Experiment1', 'experiment.json')
TEST_SAMPLESHEET1 = os.path.join(FIXTURES_DIR, 'experiments', 'Experiment1', 'SampleSheet.csv')
TEST_SAMPLESHEET2 = os.path.join(FIXTURES_DIR, 'experiments', 'Experiment2', 'SampleSheet.csv')
TEST_EXPERIMENT_DIR2 = os.path.join(TEST_EXPERIMENTS_DIR, 'Experiment2')

@override_settings(MEDIA_ROOT = MEDIA_ROOT_TEST)
class TestImporter(TestCase):
    databases = '__all__'

    @classmethod
    def tearDownClass(cls):
        # cleanup goes here
        if os.path.exists(MEDIA_ROOT_TEST):
            shutil.rmtree(MEDIA_ROOT_TEST)
        super().tearDownClass()

    def test_true(self):
        """
        demo true test to show that tests work
        """
        self.assertTrue(True)

    def test_import_experimentFoo(self):
        experiment_instance, created = importer.import_experiment(experiment_id = "ExperimentFoo", experiment_type = "NGS580")
        self.assertTrue(created)
        self.assertTrue(experiment_instance.type == 'NGS580')
        self.assertTrue(experiment_instance.experiment_id == 'ExperimentFoo')
        experiment_instance2 = Experiment.objects.get(experiment_id = 'ExperimentFoo')
        self.assertTrue(experiment_instance2.type == 'NGS580')

    def test_load_experiment_json1(self):
        json_str = '{"experiment_id":"Foo", "type":"NGS629", "bar":"baz"}'
        data = json.loads(json_str)
        self.assertTrue(data["experiment_id"] == "Foo")
        self.assertTrue(data["type"] == "NGS629")

    def test_load_experiment_json2(self):
        # {'experiment_id': 'Experiment1', 'type': 'FUSION-SEQer'}
        with open(TEST_EXPERIMENT_JSON1) as f:
            data = json.load(f)
        self.assertTrue(data["experiment_id"] == "Experiment1")
        self.assertTrue(data["type"] == "FUSION-SEQer")
        self.assertTrue(data.get("bar", "no_value") == "no_value")

    def test_load_experiment_from_jsonfile1(self):
        # {'experiment_id': 'Experiment1', 'type': 'FUSION-SEQer'}
        experiment_instance, created = importer.import_experiment_from_json_file(json_file = TEST_EXPERIMENT_JSON1)
        self.assertTrue(created)
        self.assertTrue(experiment_instance.type == 'FUSION-SEQer')

    def test_get_sampleIDs_from_samplesheet1(self):
        expected_sample_ids = ['NTC-1-H2O', 'NTC-2-H2O', 'SC-SERACARE', 'NC-HAPMAP', 'SampleAJ2', 'SampleAJ3', 'SampleAJ4', 'SampleAJ5', 'SampleAJ6', 'SampleAJ7', 'SampleAJ8', 'SampleAJ9', 'SampleAJ10', 'SampleAJ11', 'SampleAJ12', 'SampleAJ13', 'SampleAJ14', 'SampleAJ15', 'SampleAJ16', 'SampleAJ17', 'SampleAJ18', 'SampleAJ19', 'SampleAJ20', 'SampleAJ21', 'SampleAJ22', 'SampleAJ23', 'SampleAJ24', 'SampleAJ25', 'SampleAJ26', 'SampleAJ27', 'SampleAJ28', 'SampleAJ29']
        sampleIDs = importer.get_sampleIDs_from_samplesheet(TEST_SAMPLESHEET1)
        self.assertTrue(expected_sample_ids == sampleIDs)

    def test_get_sampleIDs_import1(self):
        sampleIDs = importer.get_sampleIDs_from_samplesheet(TEST_SAMPLESHEET1)
        for sampleID in sampleIDs:
            sample_instance, created = importer.import_sample(sample_id = sampleID)
            self.assertTrue(created)

    def test_import_sampleIDs_and_experiment(self):
        experiment_id = "ExperimentFoo"
        experiment_type = "NGS580"
        sample_id = "NTC-1-H2O"
        sample_instance, created = importer.import_sample(sample_id = sample_id)
        self.assertTrue(created)
        experiment_instance, created = importer.import_experiment(
            experiment_id = experiment_id,
            experiment_type = experiment_type)
        self.assertTrue(created)
        sample_instance.experiment.add(experiment_instance)
        all_experiment_ids = [ e.experiment_id for e in sample_instance.experiment.all() ]
        expected_experiment_ids = [experiment_id]
        self.assertTrue(all_experiment_ids == expected_experiment_ids)

    def test_import_all_samples_from_samplesheet(self):
        experiment_id = "ExperimentFoo"
        experiment_type = "NGS580"
        expected_sample_ids = [
            'NC-IVS35', 'Patient1', 'Patient2', 'Patient3', 'NTC-H2O'
        ]
        import_results = importer.import_from_samplesheet(
            iem_file = TEST_SAMPLESHEET2,
            experiment_id = experiment_id,
            experiment_type = experiment_type
            )
        all_imported_sampleIDs = [ s.sample_id for s in import_results[0] ]
        all_not_imported_samples = import_results[1]
        all_samples_added_experiment_querysets = [ s.experiment.all().values_list('experiment_id', flat = True) for s in import_results[2] ]
        all_samples_added_experiment_ids = []
        for e in all_samples_added_experiment_querysets:
            for exp_id in e:
                all_samples_added_experiment_ids.append(exp_id)
        all_samples_added_experiment_ids = list(set(all_samples_added_experiment_ids))
        all_samples_not_added_experiment = import_results[3]
        experiment_created = import_results[4]
        self.assertTrue(all_imported_sampleIDs == expected_sample_ids)
        self.assertTrue(all_not_imported_samples == [])
        self.assertTrue(all_samples_added_experiment_ids == [experiment_id])
        self.assertTrue(all_samples_not_added_experiment == [])
        self.assertTrue(experiment_created)

    def test_import_all_samples_from_samplesheet_dups(self):
        """
        Test that duplicates are not imported from the same samplesheet
        """
        experiment_id = "ExperimentFoo"
        experiment_type = "NGS580"
        expected_sample_ids = [
            'NC-IVS35', 'Patient1', 'Patient2', 'Patient3', 'NTC-H2O'
        ]
        # first import
        import_results = importer.import_from_samplesheet(
            iem_file = TEST_SAMPLESHEET2,
            experiment_id = experiment_id,
            experiment_type = experiment_type
            )
        all_imported_sampleIDs = [ s.sample_id for s in import_results[0] ]
        all_not_imported_samples = import_results[1]
        all_samples_added_experiment_querysets = [ s.experiment.all().values_list('experiment_id', flat = True) for s in import_results[2] ]
        all_samples_added_experiment_ids = []
        for e in all_samples_added_experiment_querysets:
            for exp_id in e:
                all_samples_added_experiment_ids.append(exp_id)
        all_samples_added_experiment_ids = list(set(all_samples_added_experiment_ids))
        all_samples_not_added_experiment = import_results[3]
        experiment_created = import_results[4]
        self.assertTrue(all_imported_sampleIDs == expected_sample_ids)
        self.assertTrue(all_not_imported_samples == [])
        self.assertTrue(all_samples_added_experiment_ids == [experiment_id])
        self.assertTrue(all_samples_not_added_experiment == [])
        self.assertTrue(experiment_created)
        # second import
        import_results = importer.import_from_samplesheet(
            iem_file = TEST_SAMPLESHEET2,
            experiment_id = experiment_id,
            experiment_type = experiment_type
            )
        all_imported_sampleIDs = [ s.sample_id for s in import_results[0] ]
        all_not_imported_samples = [ s.sample_id for s in import_results[1] ]
        all_samples_added_experiment_querysets = [ s.experiment.all().values_list('experiment_id', flat = True) for s in import_results[2] ]
        all_samples_added_experiment_ids = []
        for e in all_samples_added_experiment_querysets:
            for exp_id in e:
                all_samples_added_experiment_ids.append(exp_id)
        all_samples_added_experiment_ids = list(set(all_samples_added_experiment_ids))
        all_samples_not_added_experiment = import_results[3]
        experiment_created = import_results[4]
        self.assertTrue(all_imported_sampleIDs == [])
        self.assertTrue(all_not_imported_samples == expected_sample_ids)
        self.assertTrue(all_samples_added_experiment_ids == [experiment_id])
        self.assertTrue(all_samples_not_added_experiment == [])
        self.assertTrue(experiment_created == False)

    def test_import_from_experiment_dir(self):
        """
        Import samples from a samplesheet using the dirname as the experiment_id
        """
        expected_experiment_id = "Experiment2"
        expected_sample_ids = [
            'NC-IVS35', 'Patient1', 'Patient2', 'Patient3', 'NTC-H2O'
        ]
        import_results = importer.import_from_samplesheet(
            iem_file = TEST_SAMPLESHEET2, 
            detect_experiment_json = True)
        all_imported_sampleIDs = [ s.sample_id for s in import_results[0] ]
        all_not_imported_samples = import_results[1]
        all_samples_added_experiment_querysets = [ s.experiment.all().values_list('experiment_id', flat = True) for s in import_results[2] ]
        all_samples_added_experiment_ids = []
        for e in all_samples_added_experiment_querysets:
            for exp_id in e:
                all_samples_added_experiment_ids.append(exp_id)
        all_samples_added_experiment_ids = list(set(all_samples_added_experiment_ids))
        all_samples_not_added_experiment = import_results[3]
        experiment_created = import_results[4]
        self.assertTrue(all_imported_sampleIDs == expected_sample_ids)
        self.assertTrue(all_not_imported_samples == [])
        self.assertTrue(all_samples_added_experiment_ids == [expected_experiment_id])
        self.assertTrue(all_samples_not_added_experiment == [])
        self.assertTrue(experiment_created)



