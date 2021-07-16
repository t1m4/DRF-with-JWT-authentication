from django.urls import path

from . import views

urlpatterns = [
    path('api/create_post/', views.CreatePostAPIView.as_view(), name='social_network-create_post'),
    path('api/like/', views.LikeAPIView.as_view(), name='social_network-like'),
    path('api/unlike/', views.UnlikeAPIView.as_view(), name='social_network-unlike'),
    path('api/analitics/', views.AnaliticsAPIView.as_view(), name='social_network-analitics'),
    path('api/activity/', views.ActivityAPIView.as_view(), name='social_network-activity'),
]
