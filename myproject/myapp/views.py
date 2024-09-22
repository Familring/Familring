from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Question, Answer, BucketList, Event, Photo, Album, Furniture, Family
from .serializers import UserSerializer, QuestionSerializer, BucketListSerializer, EventSerializer, PhotoSerializer, \
    FurnitureSerializer
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from django.shortcuts import get_object_or_404


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


#로그인
@api_view(['POST'])
def login(request):
    data = request.data
    try:
        # 입력된 username에 해당하는 사용자 가져오기
        user = User.objects.get(username=data['username'])
    except User.DoesNotExist:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

    # 입력된 비밀번호 확인
    if check_password(data['password'], user.password):
        # 세션에 사용자 정보 저장
        request.session['user_id'] = user.user_id
        request.session['username'] = user.username
        request.session.save()  # 세션 강제 저장

        # 사용자에 연결된 family 정보 가져오기
        family = Family.objects.filter(user=user).first()
        if family:
            request.session['family_id'] = family.family_id


        print("세션 저장 후 확인:", request.session.get('user_id'), request.session.get('family_id'))

        return Response({
            'success': 'Login successful',
            'user_id': user.user_id,
            'username': user.username,
            'family_id': family.family_id if family else None
        }, status=status.HTTP_200_OK)
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

# 버킷리스트 가져오기
@api_view(['GET'])
def get_family_bucketlist(request):
    # 세션에서 사용자 정보 가져오기
    user_id = request.session.get('user_id')
    family_id = request.session.get('family_id')
    print(dir(request.session.get))
    print(user_id)
    print(family_id)
    # family_id를 이용해 family 객체 가져오기
    family = get_object_or_404(Family, id=family_id)

    # family에 속한 버킷리스트 가져오기
    bucketlist = BucketList.objects.filter(family=family)
    serializer = BucketListSerializer(bucketlist, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# 버킷리스트 추가하기
@api_view(['POST'])
def add_bucketlist(request):
    # 세션에서 사용자 정보 가져오기
    user_id = request.session.get('user_id')
    family_id = request.session.get('family_id')

    # family_id를 이용해 family 객체 가져오기
    family = get_object_or_404(Family, id=family_id)

    # 요청 데이터에서 버킷리스트 정보 생성
    data = {
        'family': family.family_id,  # family_id 설정
        'bucket_title': request.data['bucket_title'],
        'bucket_content': request.data.get('bucket_content', ''),
        'is_completed': False,  # 기본값으로 완료되지 않은 상태
    }
    serializer = BucketListSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 버킷리스트 완료 처리
@api_view(['PUT'])
def complete_bucketlist(request, bucket_id):
    # 세션에서 사용자 정보 가져오기
    user_id = request.session.get('user_id')
    family_id = request.session.get('family_id')

    # family_id를 이용해 family 객체 가져오기
    family = get_object_or_404(Family, id=family_id)

    # bucket_id에 해당하는 버킷리스트 항목을 완료 처리
    bucketlist = get_object_or_404(BucketList, id=bucket_id, family=family)
    bucketlist.is_completed = True
    bucketlist.save()
    return Response({"message": "버킷리스트가 완료되었습니다."}, status=status.HTTP_200_OK)

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
