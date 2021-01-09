from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from booking_app.models import Office, Workplace, Reservation
from django.urls import reverse
from datetime import datetime, timedelta


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


class WorkplaceTestCases(APITestCase):
    create_url = '/workplace/create/'
    list_url = '/workplaces/'

    def setUp(self):
        self.user = User.objects.create_superuser(username='super_testcase', password='testcase')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_workplace(self):
        office = Office.objects.create(workplaces=5)
        data = {
            'office': office.pk,
            'price': 1000
        }
        response = self.client.post(self.create_url, data)
        workplace_one = Workplace.objects.all()[0]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(workplace_one.office.pk, data['office'])
        self.assertEqual(workplace_one.price, data['price'])

        response = self.client.post(self.create_url, data)
        workplace_two = Workplace.objects.all()[1]
        self.assertEqual(response.data['id'], workplace_two.pk)

        response = self.client.get(OfficeTestCases.list_url)
        self.assertEqual(dict(response.data[0])['workplaces_id'], [workplace_one.pk, workplace_two.pk])

    def test_workplaces_list(self):
        office = Office.objects.create(workplaces=5)
        Workplace.objects.create(office=office, price=1000)
        Workplace.objects.create(office=office, price=1000)

        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(isinstance(list(response.data), list), True)
        self.assertEqual(isinstance(dict(list(response.data)[1]), dict), True)

    def test_free_workplaces_in_range(self):
        office = Office.objects.create(workplaces=5)
        workplace_one = Workplace.objects.create(office=office, price=1000)
        workplace_two = Workplace.objects.create(office=office, price=1000)
        workplace_three = Workplace.objects.create(office=office, price=1000)
        workplace_four = Workplace.objects.create(office=office, price=1000)

        date_from = (datetime.now() + timedelta(days=6)).date()
        date_to = (datetime.now() + timedelta(days=12)).date()

        response = self.client.get(
            reverse('Free_workplaces_in_range', kwargs={'date_from': date_from, 'date_to': date_to})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        id_from_response = [response.data[workplace].get('id') for workplace in range(len(response.data))]
        self.assertEqual(id_from_response, [workplace_one.pk, workplace_two.pk, workplace_three.pk, workplace_four.pk])

        Reservation.objects.create(
            user=self.user,
            office=office,
            workplace=workplace_four,
            initial_day=datetime.now() + timedelta(days=13),
            reservation_ends=datetime.now() + timedelta(days=19)
        )

        Reservation.objects.create(
            user=self.user,
            office=office,
            workplace=workplace_one,
            initial_day=datetime.now(),
            reservation_ends=datetime.now() + timedelta(days=7)
        )

        response = self.client.get(
            reverse('Free_workplaces_in_range', kwargs={'date_from': date_from, 'date_to': date_to})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        id_from_response = [response.data[workplace].get('id') for workplace in range(len(response.data))]
        self.assertEqual(id_from_response, [workplace_two.pk, workplace_three.pk, workplace_four.pk])

        Reservation.objects.create(
            user=self.user,
            office=office,
            workplace=workplace_two,
            initial_day=datetime.now() + timedelta(days=7),
            reservation_ends=datetime.now() + timedelta(days=11)
        )
        response = self.client.get(
            reverse('Free_workplaces_in_range', kwargs={'date_from': date_from, 'date_to': date_to})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        id_from_response = [response.data[workplace].get('id') for workplace in range(len(response.data))]
        self.assertEqual(id_from_response, [workplace_three.pk, workplace_four.pk])

        Reservation.objects.create(
            user=self.user,
            office=office,
            workplace=workplace_three,
            initial_day=datetime.now() + timedelta(days=11),
            reservation_ends=datetime.now() + timedelta(days=17)
        )
        response = self.client.get(
            reverse('Free_workplaces_in_range', kwargs={'date_from': date_from, 'date_to': date_to})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        id_from_response = [response.data[workplace].get('id') for workplace in range(len(response.data))]
        self.assertEqual(id_from_response, [workplace_four.pk])

        response = self.client.get(
            reverse('Free_workplaces_in_range', kwargs={'date_from': date_to, 'date_to': date_from})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        id_from_response = [response.data[workplace].get('id') for workplace in range(len(response.data))]
        self.assertEqual(id_from_response, [workplace_one.pk, workplace_two.pk, workplace_three.pk, workplace_four.pk])


    def test_edit_workplace(self):
        office = Office.objects.create(workplaces=5)
        workplace = Workplace.objects.create(office=office, price=1000)

        response = self.client.get(reverse('WorkplaceEditView', kwargs={'pk': workplace.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], workplace.pk)

        response = self.client.patch(reverse('WorkplaceEditView', kwargs={'pk': workplace.pk}), data={'price': 1100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Workplace.objects.all().get(pk=workplace.pk).price, 1100)

        response = self.client.delete(reverse('WorkplaceEditView', kwargs={'pk': workplace.pk}))
        workplaces = Workplace.objects.all()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(list(workplaces), [])

    def test_workplace_permissions(self):
        testcase_user = User.objects.create_user(username='testcase', password='testcase')
        self.client.force_authenticate(user=testcase_user)

        office = Office.objects.create(workplaces=5)

        response = self.client.post(self.create_url, {'office': 1, 'price': 1000})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(reverse('WorkplaceEditView', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ReservationTestCases(APITestCase):
    create_url = '/reservation/create/'
    list_url = '/reservations/'

    def setUp(self):
        self.user = User.objects.create_superuser(username='super_testcase', password='testcase')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)


    def test_create_reservation(self):
        office = Office.objects.create(workplaces=5)
        workplace_one = Workplace.objects.create(office=office, price=1000)
        workplace_two = Workplace.objects.create(office=office, price=1000)

        data = {
            'user': self.user.username,
            'office': office.pk,
            'workplace': 1,
            'initial_day': str(datetime.now().date()),
            'reservation_ends': str((datetime.now() + timedelta(days=6)).date())
        }

        response = self.client.post(self.create_url, data)
        reservation = Reservation.objects.all()[0]
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(reservation.pk, 1)
        self.assertEqual(reservation.user.username, data['user'])
        self.assertEqual(reservation.office.pk, data['office'])
        self.assertEqual(reservation.workplace.pk, response.data['workplace'])
        self.assertEqual(str(reservation.initial_day), response.data['initial_day'])
        self.assertEqual(str(reservation.reservation_ends), response.data['reservation_ends'])

        data['workplace'] = workplace_two.pk
        data['initial_day'] = str((datetime.now() + timedelta(days=10)).date())
        data['reservation_ends'] = str((datetime.now() + timedelta(days=16)).date())
        response = self.client.post(self.create_url, data)
        reservation = Reservation.objects.all()[1]
        self.assertEqual(reservation.pk, 2)

        days_delta = (reservation.reservation_ends - reservation.initial_day).days
        reservation_days = [str(reservation.initial_day + timedelta(days=delta)) for delta in range(days_delta + 1)]
        self.assertEqual(reservation_days, response.data['reservation_days'])

        data['initial_day'] = str((datetime.now() + timedelta(days=7)).date())
        data['reservation_ends'] = str((datetime.now() + timedelta(days=13)).date())
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data['initial_day'] = str((datetime.now() + timedelta(days=11)).date())
        data['reservation_ends'] = str((datetime.now() + timedelta(days=15)).date())
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data['initial_day'] = str((datetime.now() + timedelta(days=13)).date())
        data['reservation_ends'] = str((datetime.now() + timedelta(days=19)).date())
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data['initial_day'] = str((datetime.now() + timedelta(days=7)).date())
        data['reservation_ends'] = str((datetime.now() + timedelta(days=22)).date())
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data['initial_day'] = str((datetime.now() + timedelta(days=61)).date())
        data['reservation_ends'] = str((datetime.now() + timedelta(days=62)).date())
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data['initial_day'] = str((datetime.now() + timedelta(days=8)).date())
        data['reservation_ends'] = str((datetime.now() + timedelta(days=7)).date())
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        data['initial_day'] = str((datetime.now() - timedelta(days=1)).date())
        data['reservation_ends'] = str((datetime.now() + timedelta(days=7)).date())
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_reservation_list(self):
        office = Office.objects.create(workplaces=5)
        workplace_one = Workplace.objects.create(office=office, price=1000)
        workplace_two = Workplace.objects.create(office=office, price=1000)
        reservation_one = Reservation.objects.create(
            user=self.user,
            office=office,
            workplace=workplace_one,
            initial_day=datetime.now().date(),
            reservation_ends=(datetime.now() + timedelta(days=6)).date()
        )
        reservation_two = Reservation.objects.create(
            user=self.user,
            office=office,
            workplace=workplace_two,
            initial_day=datetime.now().date(),
            reservation_ends=(datetime.now() + timedelta(days=6)).date()
        )
        reservation_three = Reservation.objects.create(
            user=self.user,
            office=office,
            workplace=workplace_two,
            initial_day=(datetime.now() + timedelta(days=6)).date(),
            reservation_ends=(datetime.now()+ timedelta(days=7)).date()
        )
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(isinstance(list(response.data), list), True)
        self.assertEqual(isinstance(dict(list(response.data)[1]), dict), True)

        response = self.client.get(reverse('ReservationsWithWorkplaceView', kwargs={'pk': workplace_two.pk}))
        id_from_response = [response.data[reservation].get('id') for reservation in range(len(response.data))]
        self.assertEqual(id_from_response, [reservation_two.pk, reservation_three.pk])

    def test_edit_reservation(self):
        office = Office.objects.create(workplaces=5)
        workplace_one = Workplace.objects.create(office=office, price=1000)
        reservation_one = Reservation.objects.create(
            user=self.user,
            office=office,
            workplace=workplace_one,
            initial_day=datetime.now().date(),
            reservation_ends=(datetime.now() + timedelta(days=6)).date()
        )
        reservation_two = Reservation.objects.create(
            user=self.user,
            office=office,
            workplace=workplace_one,
            initial_day=(datetime.now() + timedelta(days=7)).date(),
            reservation_ends=(datetime.now() + timedelta(days=13)).date()
        )
        response = self.client.get(reverse('ReservationEditView', kwargs={'pk': reservation_one.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], reservation_one.pk)

        response = self.client.patch(reverse(
            'ReservationEditView',
            kwargs={'pk': reservation_one.pk}),
            data={'initial_day': str((datetime.now() + timedelta(days=1)).date())}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reservation_initial_day = Reservation.objects.all().get(pk=reservation_one.pk).initial_day
        self.assertEqual(reservation_initial_day, (datetime.now() + timedelta(days=1)).date())

        response = self.client.patch(reverse(
            'ReservationEditView',
            kwargs={'pk': reservation_one.pk}),
            data={'reservation_ends': str((datetime.now() + timedelta(days=7)).date())}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.delete(reverse('ReservationEditView', kwargs={'pk': reservation_one.pk}))
        response = self.client.delete(reverse('ReservationEditView', kwargs={'pk': reservation_two.pk}))
        reservations = Reservation.objects.all()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(self.list_url)
        self.assertEqual(list(reservations), list(response.data))

    def test_reservation_permissions(self):
        testcase_user = User.objects.create_user(username='testcase', password='testcase')
        self.client.force_authenticate(user=testcase_user)

        office = Office.objects.create(workplaces=5)
        workplace_one = Workplace.objects.create(office=office, price=1000)
        workplace_two = Workplace.objects.create(office=office, price=1000)
        reservation = Reservation.objects.create(
            user=self.user,
            office=office,
            workplace=workplace_one,
            initial_day=datetime.now().date(),
            reservation_ends=(datetime.now() + timedelta(days=6)).date()
        )
        response = self.client.patch(reverse(
            'ReservationEditView',
            kwargs={'pk': reservation.pk}),
            data={'workplace': workplace_two.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete(reverse('ReservationEditView', kwargs={'pk': reservation.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
