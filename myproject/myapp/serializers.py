from rest_framework import serializers
from .models import User, BucketList

# 사용자 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
<<<<<<< HEAD
        fields = ['id', 'username', 'email', 'password', 'nickname', 'is_active', 'is_staff', 'is_superuser', 'last_login']
=======
        fields = ['id', 'username', 'password',]

# 질문 시리얼라이저
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

# 답변 시리얼라이저
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
>>>>>>> b23ec16415797515489362bf40c56b9a772c0740

# 버킷리스트 시리얼라이저
class BucketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BucketList
        fields = '__all__'

