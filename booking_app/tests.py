from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status


class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {
            'username': 'testcase',
            'email': 'testcase@test.test',
            'password': '321SomePSWD123'
        }
        response = self.client.post('/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
