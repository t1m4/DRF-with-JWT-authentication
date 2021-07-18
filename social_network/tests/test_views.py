from django.test import TransactionTestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APITransactionTestCase

from authentication.models import User
from social_network.models import Post


class AuthAPITransactionTestCase(APITransactionTestCase):
    """
    Class for register user with APITransactionTestCase
    """
    register_url = reverse('authentication-register')
    user_one = {
        'email': 'test1@mail.ru',
        'username': 'test1',
        'password': 'alksdfjs',
        'double_password': 'alksdfjs',
    }

    def register(self):
        response = self.client.post(self.register_url, self.user_one)
        data = response.json()
        self.access = data['access']
        self.refresh = data['refresh']
        # save credentials
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access)


class CreatePostTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        """
        setup data for whole class
        """
        cls.create_post_url = reverse('social_network-create_post')
        cls.user_one = {
            'email': 'test1@mail.ru',
            'username': 'test1',
            'password': 'alksdfjs',
        }
        u = User.objects.create(**cls.user_one)
        cls.access = u.tokens['access']

    def setUp(self):
        self.post_data = {
            'id': 2,
            'title': 'title',
            'description': 'description'
        }
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access)

    def test_cannot_create_post_without_authorization(self):
        self.client.credentials()
        response = self.client.post(self.create_post_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cannot_create_post_without_data(self):
        response = self.client.post(self.create_post_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_post_with_invalid_fields(self):
        data = self.post_data
        data.pop('title')
        response = self.client.post(self.create_post_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_create_post(self):
        response = self.client.post(self.create_post_url, self.post_data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get('title'), self.post_data.get('title'))
        self.assertEqual(data.get('description'), self.post_data.get('description'))


def like_and_unlike_setUp(self):
    self.create_post_url = reverse('social_network-create_post')
    self.like_url = reverse('social_network-like')
    self.unlike_url = reverse('social_network-unlike')
    user_one = {
        'email': 'test1@mail.ru',
        'username': 'test1',
        'password': 'alksdfjs',
    }
    u = User.objects.create(**user_one)
    self.client.credentials(HTTP_AUTHORIZATION="Bearer " + u.tokens['access'])

    post_one = {
        'user': u,
        'title': 'title',
        'description': 'description',
    }
    post_id = Post.objects.create(**post_one).id
    self.like_data = {
        'post_id': post_id
    }


class LikeTest(APITransactionTestCase):

    def setUp(self):
        like_and_unlike_setUp(self)

    def test_cannot_like_without_data(self):
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_like_without_authorization(self):
        self.client.credentials()
        response = self.client.post(self.like_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_like(self):
        response = self.client.post(self.like_url, self.like_data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(data.get('create_at'))

    def test_cannot_like_if_already_like(self):
        self.client.post(self.like_url, self.like_data)
        response = self.client.post(self.like_url, self.like_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_like_not_exists_post(self):
        self.like_data['post_id'] = 2
        self.client.post(self.like_url, self.like_data)
        response = self.client.post(self.like_url, self.like_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UnlikeTest(APITransactionTestCase):
    def setUp(self):
        like_and_unlike_setUp(self)

    # unlike tests
    def test_cannot_unlike_without_data(self):
        self.client.post(self.like_url, self.like_data)
        response = self.client.post(self.unlike_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_unlike_without_authorization(self):
        self.client.credentials()
        self.client.post(self.like_url, self.like_data)
        response = self.client.post(self.unlike_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_unlike(self):
        self.client.post(self.like_url, self.like_data)
        response = self.client.post(self.unlike_url, self.like_data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cannot_unlike_if_not_exist_like(self):
        response = self.client.post(self.unlike_url, self.like_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_unlike_not_exists_post(self):
        self.like_data['post_id'] += 1
        self.client.post(self.unlike_url, self.like_data)
        response = self.client.post(self.like_url, self.like_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
