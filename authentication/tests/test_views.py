from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationTest(APITestCase):
    def setUp(self):
        self.register_url = reverse('social_network-register')
        self.login_url = reverse('social_network-login')
        self.register_data = {
            'email': 'test@mail.ru',
            'username': 'test',
            'password': 'password',
            'double_password': 'password',
        }
        self.login_data = {
            'username': 'test',
            'password': 'password',
        }

    def test_user_cannot_register_without_data(self):
        response = self.client.post(self.register_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_register(self):
        response = self.client.post(self.register_url, data=self.register_data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get('username'), self.register_data.get('username'))
        self.assertEqual(data.get('email'), self.register_data.get('email'))
        self.assertIsNone(data.get('password'))
        self.assertIsNotNone(data.get('refresh'))
        self.assertIsNotNone(data.get('access'))

    def test_user_cannot_login_without_data(self):
        response = self.client.post(self.login_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_cannot_login_with_invalid_username(self):
        # register
        self.client.post(self.register_url, self.register_data)

        # login
        self.login_data['username'] = 'invalid'
        response= self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_user_cannot_login_with_invalid_password(self):
        # register
        self.client.post(self.register_url, self.register_data)

        # login
        self.login_data['password'] = 'invalid'
        response= self.client.post(self.login_url, self.login_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_login(self):
        # register
        self.client.post(self.register_url, self.register_data)

        # login
        response = self.client.post(self.login_url, self.login_data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(data.get('refresh'))
        self.assertIsNotNone(data.get('access'))
