from django.urls import path
from rest_framework_simplejwt import views as jwt_views

from . import views

urlpatterns = [
    # path('api/login/', views.ThrottleTokenObtainPairView.as_view(), name='social_network-login'),
]


