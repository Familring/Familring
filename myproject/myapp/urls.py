from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    register, login, get_daily_question, submit_answer,
      get_family_events, add_event,
    get_album_photos, upload_photo, add_furniture, get_family_furniture
    ,get_family_bucketlist, add_bucketlist, complete_bucketlist

)

urlpatterns = [
    # 회원관리
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    # 질문
    path('daily-question/', get_daily_question, name='get_daily_question'),
    path('submit-answer/<int:question_id>/', submit_answer, name='submit_answer'),

    # 버킷리스트
    path('bucket/', get_family_bucketlist, name='get_family_bucketlist'),
    path('bucket/add/', add_bucketlist, name='add_bucketlist'),
    path('bucket/complete/<int:bucket_id>/', complete_bucketlist, name='complete_bucketlist'),
    # 일정
    path('events/', get_family_events, name='get_family_events'),
    path('add-event/', add_event, name='add_event'),

    # 사진 앨범
    path('album/<int:album_id>/photos/', get_album_photos, name='get_album_photos'),
    path('album/<int:album_id>/upload/', upload_photo, name='upload_photo'),

    # 가구 (스티커)
    path('add-furniture/', add_furniture, name='add_furniture'),
    path('family-furniture/', get_family_furniture, name='get_family_furniture'),
]
