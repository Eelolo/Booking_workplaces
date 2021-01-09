from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data = {
            'username': 'testcase',
            'email': 'testcase@test.test',
            'password': '321SomePSWD123'
        }
        response = self.client.post('/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AuthenticationTestCase(APITestCase):
    login_url = '/token/login/'
    get_users_url = '/users/'

    def setUp(self):
        self.user = User.objects.create_user(username='testcase', password='testcase')
        self.token = Token.objects.create(user=self.user)

    def test_authentication(self):
        data = {
            'username': 'testcase',
            'password': 'testcase'
        }
        wrong_data = {
            'username': 'case',
            'password': 'testcase'
        }

        response = self.client.post(self.login_url, wrong_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['auth_token'], self.token.key)

    def test_authorization(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.get_users_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(self.get_users_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['username'], self.user.username)