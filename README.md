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
<p>Install all requirements</p>
<code>pip install requirements.txt</code>
<p>Run tests...</p>
<code>python manage.py test</code>
<p>And if everything all right start server</p>
<code>python manage.py runserver</code>



<h1>Basic API Features</h1>
<h3>Post creation using POST request</h3>

<p>1. </p>

<h1>Authentication Using JWT</h1>
<p>1. Override default User model</p>
<p>2. Override default UserManager model</p>
<p>3. Add rest_framework_simplejwt library </p>
<code> INSTALLED_APPS += [
    'rest_framework_simplejwt'
]</code>



<h1>Security Tips</h1>
<p>1. Сheck password strength</p>
<p>2. Add lifetime for tokens</p>
<code>SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
</code>
<p>3. Add throttling to your views. Configure it for yourself.</p>
```REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '50/day',
        'user': '1000/day'
    }
```
`class RegisterAPIView(APIView):
    throttle_classes = [AnonRateThrottle]
`
