from django.test import TestCase
from .models import Experiment, Sample, SampleExperiment

# Create your tests here.
class TestLIMS(TestCase):
    databases = '__all__'
    @classmethod # causes setup to only run once per instance of this class, instead of before every test
    def setUpTestData(self):
        # make demo fake db entries
        exp1_instance = Experiment.objects.create(experiment_id = 'Experiment1', type = 'NGS580')
        instance = Experiment.objects.create(experiment_id = 'Experiment2', type = 'FUSION-SEQer')
        instance = Experiment.objects.create(experiment_id = 'Experiment3', type = 'NGS580')
        instance = Experiment.objects.create(experiment_id = 'Experiment4', type = 'NGS629')
        sample1_instance = Sample.objects.create(sample_id = 'Sample1')
        SampleExperiment.objects.create(sample_id = sample1_instance, experiment_id = exp1_instance)

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
        instance = SampleExperiment.objects.get(sample_id = sample1_instance, experiment_id = exp1_instance)
        self.assertTrue(instance.sample_id.sample_id == 'Sample1')
        self.assertTrue(instance.experiment_id.experiment_id == 'Experiment1')
        self.assertTrue(instance.experiment_id.type == 'NGS580')
