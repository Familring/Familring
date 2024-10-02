from rest_framework import serializers
from .models import User, Question, Answer, BucketList, Event, Photo, Album, Comment, Furniture

# 사용자 시리얼라이저
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
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

# 버킷리스트 시리얼라이저
class BucketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BucketList
        fields = '__all__'

# 이벤트(캘린더) 시리얼라이저
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

# 사진 시리얼라이저
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = '__all__'

# 앨범 시리얼라이저
class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'

# 댓글 시리얼라이저
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

# 가구(스티커) 시리얼라이저
class FurnitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Furniture
        fields = '__all__'
