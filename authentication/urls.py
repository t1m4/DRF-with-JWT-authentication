from django.conf.urls import url
from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    # path('api/login/', views.ThrottleTokenObtainPairView.as_view(), name='social_network-login'),
    path('api/login/', views.LoginAPIView.as_view(), name='social_network-login'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='social_network-refresh'),
    path('api/register/', views.RegistrationAPIView.as_view(), name='social_network-register'),
    path('hello/', views.HelloView.as_view(), name='hello'),
]


