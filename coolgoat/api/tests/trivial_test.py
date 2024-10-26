from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class GetFixturesTest(APITestCase):
    def test_get_fixtures(self):
        url = reverse('match-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)