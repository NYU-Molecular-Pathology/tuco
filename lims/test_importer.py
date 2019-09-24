import os
import sys
from django.test import TestCase

this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, this_dir)
import importer
sys.path.pop(0)

class TestImporter(TestCase):
    databases = '__all__'

    def test_true(self):
        """
        demo true test to show that tests work
        """
        self.assertTrue(True)
