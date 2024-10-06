from rest_framework import serializers
from .models import User, BucketList

# 사용자 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'nickname', 'is_active', 'is_staff', 'is_superuser', 'last_login']

# 버킷리스트 시리얼라이저
class BucketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BucketList
        fields = '__all__'

