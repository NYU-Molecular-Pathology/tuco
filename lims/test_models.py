import os
from django.test import TestCase, override_settings
from django.core.files import File
from .models import Experiment, Sample, SampleExperiment, Samplesheet
from django.conf import settings
import shutil
# https://docs.djangoproject.com/en/2.2/topics/testing/tools/

# location for media uploads during testing
MEDIA_ROOT_TEST = os.path.realpath(os.environ['MEDIA_ROOT_TEST'])
FIXTURES_DIR = os.path.realpath(os.environ['FIXTURES_DIR'])
TEST_SAMPLESHEET1 = os.path.join(FIXTURES_DIR, 'experiments', 'Experiment1', 'SampleSheet.csv')

@override_settings(MEDIA_ROOT = MEDIA_ROOT_TEST)
class TestLIMS(TestCase):
    databases = '__all__'

    @classmethod # causes setup to only run once per instance of this class, instead of before every test
    def setUpTestData(cls):
        # make demo fake db entries
        exp1_instance = Experiment.objects.create(experiment_id = 'Experiment1', type = 'NGS580')
        instance = Experiment.objects.create(experiment_id = 'Experiment2', type = 'FUSION-SEQer')
        instance = Experiment.objects.create(experiment_id = 'Experiment3', type = 'NGS580')
        instance = Experiment.objects.create(experiment_id = 'Experiment4', type = 'NGS629')
        sample1_instance = Sample.objects.create(sample_id = 'Sample1')
        SampleExperiment.objects.create(sample = sample1_instance, experiment = exp1_instance)
        Samplesheet.objects.create(experiment = exp1_instance,
            file = File(open(TEST_SAMPLESHEET1), name = TEST_SAMPLESHEET1) )

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

    def test_get_Experiment1(self):
        # test that you can get a specific experiment instance out of the database by run_ID
        instance = Experiment.objects.get(experiment_id = 'Experiment1')
        self.assertTrue(instance.experiment_id == 'Experiment1')

    def test_get_Experiment_type(self):
        # test that the experiment instances types match expected values
        instance = Experiment.objects.get(experiment_id = 'Experiment2')
        self.assertTrue(instance.type == 'FUSION-SEQer')
        instance = Experiment.objects.get(experiment_id = 'Experiment3')
        self.assertTrue(instance.type == 'NGS580')
        instance = Experiment.objects.get(experiment_id = 'Experiment4')
        self.assertTrue(instance.type == 'NGS629')

    def test_get_sample1(self):
        # test that you can get a specific sample instance out of the database by run_ID
        instance = Sample.objects.get(sample_id = 'Sample1')
        self.assertTrue(instance.sample_id == 'Sample1')

    def test_get_sample_experiment1(self):
        # test that you can get a specific sample_experiment instance out of the database by run_ID
        sample1_instance = Sample.objects.get(sample_id = 'Sample1')
        exp1_instance = Experiment.objects.get(experiment_id = 'Experiment1', type = 'NGS580')
        sample_experiment_instance = SampleExperiment.objects.get(sample = sample1_instance, experiment = exp1_instance)
        self.assertTrue(sample_experiment_instance.sample.sample_id == 'Sample1')
        self.assertTrue(sample_experiment_instance.experiment.experiment_id == 'Experiment1')
        self.assertTrue(sample_experiment_instance.experiment.type == 'NGS580')

    def test_samplesheet1(self):
        # test that an imported samplesheet entry exists
        exp1_instance = Experiment.objects.get(experiment_id = 'Experiment1', type = 'NGS580')
        samplesheet_instance = Samplesheet.objects.get(experiment = exp1_instance)
        self.assertTrue(samplesheet_instance.experiment.experiment_id == 'Experiment1')
        samplesheet_path = os.path.join(settings.MEDIA_ROOT, samplesheet_instance.file.name)
        self.assertTrue(samplesheet_path)
