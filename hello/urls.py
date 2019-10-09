from django.urls import path
from hello import views
from hello.controllers import topicController, pictureController, commentController
from django.contrib import admin
from django.urls import include, path, re_path

import re

from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path("bam/", views.home, name="home"),
    path('api/topics/', topicController.Topics.as_view(), name='Topics'),
    path('api/topics/<str:topicName>/', topicController.TopicController.as_view(), name='Topics'),

    path('api/topics/<str:topicName>/pictures/',
         pictureController.Pictures.as_view(), name='Pictures'),

    path('api/topics/<str:topicName>/pictures/<int:pictureID>/',
         pictureController.PictureController.as_view(), name='Pictures'),

    path('api/topics/<str:topicName>/pictures/<int:pictureID>/comments/',
         commentController.Comments.as_view(), name='Comments'),

    path('api/topics/<str:topicName>/pictures/<int:pictureID>/comments/<int:commentID>/',
         commentController.CommentController.as_view(), name='Comments'),

    path('hello/', views.HelloView.as_view(), name='hello'),

    
    re_path(r"^admin/", admin.site.urls),
    re_path(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(),
         name='token_refresh'),
]
