from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    path('api/login/', views.LoginAPIView.as_view(), name='authentication-login'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='authentication-refresh'),
    path('api/register/', views.RegistrationAPIView.as_view(), name='authentication-register'),
    path('api/test/', views.HelloView.as_view(), name='authentication-test'),
]
