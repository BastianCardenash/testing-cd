from unittest.mock import patch
from django.test import TestCase
import requests

class SimpleTest(TestCase):
    # @patch('api.views.MatchListView.get')
    # @patch('requests.get')
    def test_basic_math(self):
        self.assertEqual(1 + 1, 2)
        print("Test passed")