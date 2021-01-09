from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from booking_app.models import Office, Workplace
from django.urls import reverse



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


class OfficeTestCases(APITestCase):
    create_url = '/office/create/'
    list_url = '/offices/'

    def setUp(self):
        self.user = User.objects.create_superuser(username='super_testcase', password='testcase')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_office(self):
        data = {
            'workplaces': 5
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        office = Office.objects.all()[0]
        self.assertEqual(office.pk, 1)
        self.assertEqual(office.workplaces, data['workplaces'])
        self.assertEqual(response.data['workplaces_id'], [])

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.data['id'], 2)

    def test_offices_list(self):
        Office.objects.create(workplaces=5)
        Office.objects.create(workplaces=5)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(isinstance(list(response.data), list), True)
        self.assertEqual(isinstance(dict(list(response.data)[1]), dict), True)

    def test_edit_office(self):
        office = Office.objects.create(workplaces=5)

        response = self.client.get(reverse('OfficeEditView', kwargs={'pk': office.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], Office.objects.all()[0].pk)

        response = self.client.patch(reverse('OfficeEditView', kwargs={'pk': office.pk}), data={'workplaces': 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        office = Office.objects.all().get(pk=office.pk)
        self.assertEqual(office.workplaces, 10)

        response = self.client.delete(reverse('OfficeEditView', kwargs={'pk': office.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        workplaces = Workplace.objects.all()
        self.assertEqual(list(workplaces), [])

    def test_office_permissions(self):
        testcase_user = User.objects.create_user(username='testcase', password='testcase')
        self.client.force_authenticate(user=testcase_user)

        response = self.client.post(self.create_url, {'workplaces': 5})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(reverse('OfficeEditView', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)