from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class APICallTestCase(APITestCase):

    def test_api_call(self):
        url = 'https://www.trycoz.me/api/fixtures/'
        response = self.client.get(url)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)