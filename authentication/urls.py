from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('api/login/', jwt_views.TokenObtainPairView.as_view(), name='authentication-login'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='authentication-refresh'),
    path('api/register/', views.RegistrationAPIView.as_view(), name='authentication-register'),
    path('hello/', views.HelloView.as_view(), name='hello'),
]