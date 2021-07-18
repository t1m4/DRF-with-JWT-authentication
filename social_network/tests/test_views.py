from datetime import datetime, timedelta

from django.urls import reverse
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.test import APITestCase, APITransactionTestCase

from authentication.models import User
from social_network.models import Post, Like


class CreatePostViewTest(APITestCase):

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


class LikeViewTest(APITransactionTestCase):

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


class UnlikeViewTest(APITransactionTestCase):
    def setUp(self):
        like_and_unlike_setUp(self)

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


class AnalyticsViewTest(APITestCase):
    """
    If each user like his every post and another user like half his posts:
        All like - users_count * posts_count + users_count * int(posts_count / 2)
        analytics return count - posts_count + int(posts_count / 2)

    If each user like his every post and another user like every his posts:
        All like - 2 * users_count * posts_count
        analytics return count - 2 * posts_count

    If each user like his every post and each other users like every his posts:
        All like - users_count * users_count * posts_count
        analytics return count - users_count * posts_count
    """
    users_count = 3
    posts_count = 4

    # if all posts likes for next user - posts_count + posts_count
    def setUp(self):
        self.analytics_url = reverse('social_network-analytics')
        self.date_from = "2021-07-01"
        self.date_to = "2021-07-25"
        self.params = "?date_from={date_from}&date_to={date_to}".format(date_from=self.date_from, date_to=self.date_to)

        users = self.create_users()

        for i in range(self.users_count):
            user = users[i]
            # like half posts for the next user
            # posts = users[(i + 1) % self.users_count].post_set.all()[:int(self.posts_count / 2)]
            posts = users[(i + 1) % self.users_count].post_set.all()
            for post in posts:
                like = Like.objects.create(user=user, post=post)
                like.create_at = make_aware(datetime(year=2021, month=7, day=12))
                like.save()

        self.auth_user = users[0]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.auth_user.tokens['access'])

    def create_users(self):
        """
        create user and its post and like it
        """
        user_data = {
            'email': 'test_0@mail.ru',
            'username': 'test_0',
            'password': 'alksdfjs',
        }
        post_data = {
            'user': 'user',
            'title': 'title_0',
            'description': 'description',
        }
        users = []

        for i in range(self.users_count):
            user_data['email'] = user_data['email'].replace(str(i), str(i + 1))
            user_data['username'] = user_data['username'].replace(str(i), str(i + 1))
            user = User.objects.create(**user_data)
            users.append(user)

            post_data['user'] = user
            # create post for user and like it.
            for i in range(self.posts_count):
                post_data['title'] = post_data['title'].replace(str(i), str(i + 1))
                post = Post.objects.create(**post_data)
                like = Like.objects.create(user=user, post=post)
                like.create_at = make_aware(datetime.now() + timedelta(days=i))
                like.save()
        return users

    def test_cannot_get_without_data(self):
        response = self.client.get(self.analytics_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_analytics_without_authorization(self):
        self.client.credentials()
        response = self.client.get(self.analytics_url + self.params)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_get_analytics(self):
        response = self.client.get(self.analytics_url + self.params)
        data = response.json()

        like_count = 0
        for i in data:
            day = datetime.strptime(i.get('day'), "%Y-%m-%d")
            # get every like with this user and in this range date
            likes = Like.objects.filter(post__user=self.auth_user, create_at__year=day.year,
                                        create_at__month=day.month, create_at__day=day.day)
            day_likes = i.get('count')
            self.assertEqual(likes.count(), day_likes)
            like_count += day_likes

    def test_cannot_if_likes_not_exist(self):
        Like.objects.all().delete()
        response = self.client.get(self.analytics_url + self.params)
        data = response.json()
        self.assertEqual(data, [])

    def test_cannot_get_analytics_with_invalid_date(self):
        self.params = self.params.replace(self.date_from, self.date_from +"1")
        response = self.client.get(self.analytics_url + self.params)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
