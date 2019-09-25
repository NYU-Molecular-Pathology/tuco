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
        experiment_instance, created = importer.import_experiment(experiment_id = "ExperimentFoo", type = "NGS580")
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
