from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Question, Answer, BucketList, Event, Photo, Album, Furniture
from .serializers import UserSerializer, QuestionSerializer, AnswerSerializer, BucketListSerializer, EventSerializer, PhotoSerializer, AlbumSerializer, FurnitureSerializer
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime

# 회원가입
@api_view(['POST'])
def register(request):
    data = request.data.copy()
    data['password'] = make_password(data['password'])
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 로그인
@api_view(['POST'])
def login(request):
    data = request.data
    try:
        user = User.objects.get(username=data['username'])
    except User.DoesNotExist:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

    if check_password(data['password'], user.password):
        return Response({'success': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

# 질문 관련 기능
@api_view(['GET'])
def get_daily_question(request):
    today = datetime.today().date()
    question = Question.objects.filter(created_at=today).first()
    if not question:
        return Response({"error": "오늘의 질문이 아직 생성되지 않았습니다."}, status=status.HTTP_404_NOT_FOUND)
    serializer = QuestionSerializer(question)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def submit_answer(request, question_id):
    user = request.user
    question = Question.objects.get(id=question_id)
    answer = Answer.objects.create(
        user=user,
        question=question,
        text_a=request.data['answer']
    )
    return Response({"message": "답변이 등록되었습니다."}, status=status.HTTP_201_CREATED)

# 버킷리스트 기능
@api_view(['GET', 'POST'])
def bucket_list(request):
    if request.method == 'POST':
        serializer = BucketListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'GET':
        bucket_list = BucketList.objects.all()
        serializer = BucketListSerializer(bucket_list, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def get_family_bucketlist(request):
    family = request.user.family
    bucketlist = BucketList.objects.filter(family=family)
    serializer = BucketListSerializer(bucketlist, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_bucketlist(request):
    family = request.user.family
    bucketlist = BucketList.objects.create(
        family=family,
        bucket_title=request.data['bucket_title'],
        bucket_content=request.data['bucket_content'],
        is_completed=request.data.get('is_completed', False)
    )
    return Response({"message": "버킷리스트가 추가되었습니다."}, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
def complete_bucketlist(request, bucket_id):
    try:
        bucketlist = BucketList.objects.get(id=bucket_id, family=request.user.family)
        bucketlist.is_completed = True
        bucketlist.save()
        return Response({"message": "버킷리스트 항목이 완료되었습니다."}, status=status.HTTP_200_OK)
    except BucketList.DoesNotExist:
        return Response({"error": "해당 버킷리스트 항목을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

# 일정 관리 기능
@api_view(['GET'])
def get_family_events(request):
    family = request.user.family
    events = Event.objects.filter(family=family)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def add_event(request):
    family = request.user.family
    event = Event.objects.create(
        family=family,
        event_title=request.data['title'],
        event_content=request.data['content'],
        start_date=request.data['start_date'],
        end_date=request.data['end_date']
    )
    return Response({"message": "일정이 추가되었습니다."}, status=status.HTTP_201_CREATED)

# 사진 앨범 기능
@api_view(['GET'])
def get_album_photos(request, album_id):
    album = Album.objects.get(id=album_id, family=request.user.family)
    photos = Photo.objects.filter(album=album)
    serializer = PhotoSerializer(photos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def upload_photo(request, album_id):
    album = Album.objects.get(id=album_id, family=request.user.family)
    photo = Photo.objects.create(
        album=album,
        user=request.user,
        image=request.data['image']
    )
    return Response({"message": "사진이 업로드되었습니다."}, status=status.HTTP_201_CREATED)

# 스티커 (가구) 기능
@api_view(['POST'])
def add_furniture(request):
    family = request.user.family
    furniture = Furniture.objects.create(
        family=family,
        furniture_name=request.data['furniture_name'],
        position_x=request.data['position_x'],
        position_y=request.data['position_y']
    )
    return Response({"message": "가구가 추가되었습니다."}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def get_family_furniture(request):
    family = request.user.family
    furniture = Furniture.objects.filter(family=family)
    serializer = FurnitureSerializer(furniture, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
