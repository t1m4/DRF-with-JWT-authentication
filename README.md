<h1>Overview</h1>
<p>It's simple REST API for everyday social network.</p>
<p>Created using <a href="https://www.django-rest-framework.org/">Django-Rest-Framework</a> using JWT authentication</p>
<p>Basic Features:</p>
<ul>
    <li>User signup</li>
    <li>User login</li>
    <li>Post creation</li>
    <li>Like post</li>
    <li>Unlike post</li>
</ul>

<h1>Installation</h1>
1. Install all requirements.

`pip install requirements.txt`

2. Run tests...

`python manage.py test`

3. Add `.env` file to main and `automated_bot/` directories.

4. And if everything all right start server.

`python manage.py runserver`



<h1>Basic API Features</h1>
<h3>Post creation using POST request.</h3>

<p>1. Sign up example.</p>

```json
{
  "username": "test",
  "email": "test@example.com",
  "password": "password",
  "double_password": "password"
}
```
<p>2. Login example.</p>

```json
{
  "username": "test",
  "password": "password"
}
```
<p>3. Post creation example.</p>

```json
{
  "title": "test",
  "description": "I love testing!"
}
```
<p>4. Post like/unlike example.</p>

```json
{
  "post_id": "test"
}
```
<p>5. Analytics point example.</p>

```curl
GET /facebook/api/analitics/?date_from=2020-02-02&date_to=2020-02-15
```
<p>6. Activity point example.</p>

```curl
GET /facebook/api/activity/?username=test
```
```json
{
  "last_login": "2021-07-19 11:31:55",
  "last_request": "2021-07-19 11:48:37"
}
```

<h1>Authentication Using JWT</h1>
<p>1. Override default User model</p>
<p>2. Override default UserManager model</p>
<p>3. Add rest_framework_simplejwt library </p>

```python
INSTALLED_APPS += [
    'rest_framework_simplejwt'
]
```

<h1>Automated bot</h1>
1. Start bot from <code>automated_bot/</code>

```python async_bot.py```

2.The bot use data from `automated_bot/.env</` file

```python
number_of_users=5
max_posts_per_user=7
max_likes_per_user=8
```
3. Sign Up `number_of_users` users

4. Each user creates random number of posts, but maximum `max_posts_per_user` 

5. Each user randomly like `max_likes_per_user` posts


<h1>Security Tips</h1>
<p>1. Сheck  password strength</p>
<p>2. Add lifetime for tokens</p>

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```
<p>3. Add throttling to your views. Configure it for yourself.</p>

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '50/day',
        'user': '1000/day'
    }
```
```python
# views.py
class RegisterAPIView(APIView):
    throttle_classes = [AnonRateThrottle]
```
