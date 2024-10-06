from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    register, login ,get_family_bucketlist, add_bucketlist, complete_bucketlist,
    get_profile, update_profile
)

urlpatterns = [
    # 회원관리
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 버킷리스트
    path('bucket/', get_family_bucketlist, name='get_family_bucketlist'),
    path('bucket/add/', add_bucketlist, name='add_bucketlist'),
    path('bucket/complete/<int:bucket_id>/', complete_bucketlist, name='complete_bucketlist'),

    path('profile/', get_profile, name='get_profile'),
    path('profile/update/', update_profile, name='update_profile'),
]
