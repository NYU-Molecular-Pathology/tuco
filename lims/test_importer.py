import os
import sys
import json
from django.test import TestCase, override_settings
from .models import Experiment, Sample, ExperimentSample, Samplesheet
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
        data = importer.parse_experiment_json(json_str)
        self.assertTrue(data["experiment_id"] == "Foo")
        self.assertTrue(data["type"] == "NGS629")
        self.assertTrue(data.get("bar", "no_value") == "no_value")

    def test_load_experiment_json2(self):
        # {'experiment_id': 'Experiment1', 'type': 'FUSION-SEQer'}
        json_str = open(TEST_EXPERIMENT_JSON1).read()
        data = importer.parse_experiment_json(json_str)
        self.assertTrue(data["experiment_id"] == "Experiment1")
        self.assertTrue(data["type"] == "FUSION-SEQer")
        self.assertTrue(data.get("bar", "no_value") == "no_value")

    def test_load_experiment_from_jsonfile1(self):
        # {'experiment_id': 'Experiment1', 'type': 'FUSION-SEQer'}
        experiment_instance, created = importer.import_experiment_from_json(json_file = TEST_EXPERIMENT_JSON1)
        self.assertTrue(created)
        self.assertTrue(experiment_instance.type == 'FUSION-SEQer')
