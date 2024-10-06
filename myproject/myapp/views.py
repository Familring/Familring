from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, BucketList, Family, FamilyRequest, FamilyList
from .serializers import UserSerializer, BucketListSerializer, FamilySerializer, \
    FamilyRequestSerializer
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token


@api_view(['GET'])
def get_csrf_token(request):
    csrf_token = get_token(request)
    return Response({'csrfToken': csrf_token})

# 회원가입
@api_view(['POST'])
def register(request):
    data = request.data.copy()
    data['password'] = make_password(data['password'])
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([AllowAny])  # 누구나 접근 가능하게 설정
def login(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')

    # 사용자 인증
    user = authenticate(request, username=username, password=password)
    if user is not None:
        # JWT 토큰 생성
        refresh = RefreshToken.for_user(user)

        # 사용자에 연결된 family 정보 가져오기
        family = Family.objects.filter(user=user).first()
        family_id = family.family_id if family else None

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'username': user.username,
            'family_id': family_id,
        }, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)


# 버킷리스트 기능
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@api_view(['GET'])
@permission_classes([IsAuthenticated])  # 인증된 사용자만 접근 가능
def get_family_bucketlist(request):
    user = request.user
    family = Family.objects.filter(user=user).first()
    if not family:
        return Response({'error': 'No family associated with this user'}, status=status.HTTP_400_BAD_REQUEST)

    bucketlist = BucketList.objects.filter(family=family)
    serializer = BucketListSerializer(bucketlist, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK,content_type='application/json; charset=utf-8')

# 버킷리스트 추가하기
@api_view(['POST'])
@permission_classes([IsAuthenticated])  # JWT 토큰으로 인증된 사용자만 접근 가능
def add_bucketlist(request):
    # 토큰을 통해 인증된 사용자 정보 가져오기
    user = request.user

    # user와 연결된 family 정보 가져오기
    family = get_object_or_404(Family, user=user)

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
@permission_classes([IsAuthenticated])  # JWT 토큰으로 인증된 사용자만 접근 가능
def complete_bucketlist(request, bucket_id):
    # 토큰을 통해 인증된 사용자 정보 가져오기
    user = request.user
    print(bucket_id)
    # user와 연결된 family 정보 가져오기
    family = get_object_or_404(Family, user=user)

    # bucket_id에 해당하는 버킷리스트 항목을 완료 처리
    bucketlist = get_object_or_404(BucketList, id=bucket_id, family=family)
    bucketlist.is_completed = True
    bucketlist.save()
    return Response({"message": "버킷리스트가 완료되었습니다."}, status=status.HTTP_200_OK)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer

@api_view(['GET'])
def get_profile(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['PUT'])
def update_profile(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(
        serializer.data,
        status=200,
        content_type='application/json; charset=utf-8'
    )

# 사용자 검색 기능
@api_view(['GET'])
def search_user(request):
    username = request.GET.get('username')
    if not username:
        return Response(
            {'error': 'Username parameter is required'},
            status=400,
            content_type='application/json; charset=utf-8'
        )

    try:
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        return Response(
            serializer.data,
            status=200,
            content_type='application/json; charset=utf-8'
        )
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=404,
            content_type='application/json; charset=utf-8'
        )

# 가족 초대 요청 생성
@api_view(['POST'])
def send_family_invitation(request):
    data = request.data
    from_user = request.user
    to_user = get_object_or_404(User, id=data['to_user_id'])

    # from_user의 family를 가져오기
    try:
        family = Family.objects.get(user=from_user)  # Family와 User가 연결된 부분
    except Family.DoesNotExist:
        return Response({"error": "사용자의 가족 정보를 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

    # 이미 초대된 사용자인지 확인
    if FamilyRequest.objects.filter(from_user=from_user, to_user=to_user, family=family).exists():
        return Response({"error": "이미 가족 초대를 보냈습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 가족 초대 요청 생성
    FamilyRequest.objects.create(
        from_user=from_user,
        to_user=to_user,
        family=family,
        progress='진행중'
    )

    return Response({"message": "가족 초대 요청이 전송되었습니다."}, status=status.HTTP_201_CREATED)

# 가족 초대 요청 상태 확인
@api_view(['GET'])
def check_invitation_status(request):
    requests = FamilyRequest.objects.filter(to_user=request.user)
    response_data = []
    for request in requests:
        response_data.append({
            'from_user': request.from_user.nickname,
            'family_id': request.family.family_id,
            'progress': request.progress,
        })
    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def pending_family_request(request):
    """
    진행 중인 가족 초대 요청을 가져오는 API.
    로그인한 사용자에게 도착한 초대 요청이 있는지 확인합니다.
    """
    try:
        # 현재 사용자가 받은 초대 요청 중 진행중인 요청 가져오기
        pending_requests = FamilyRequest.objects.filter(to_user=request.user, progress='진행중')

        if not pending_requests.exists():
            print("????")
            return Response({"message": "진행중인 가족 초대 요청이 없습니다."}, status=status.HTTP_200_OK)

        # 여러 초대 요청 중 첫 번째 요청만 처리
        pending_request = pending_requests.first()
        serializer = FamilyRequestSerializer(pending_request)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 가족 초대 승인/거절
@api_view(['POST'])
def respond_to_invitation(request):
    data = request.data
    family_request = get_object_or_404(FamilyRequest, id=data['request_id'])

    if data['action'] == '승인':
        # FamilyList에 추가
        FamilyList.objects.create(
            family=family_request.family,
            user=request.user
        )
        family_request.progress = '승인'
        family_request.save()
        return Response({"message": "가족 초대가 승인되었습니다."}, status=status.HTTP_200_OK)
    elif data['action'] == '거절':
        family_request.progress = '거절'
        family_request.save()
        return Response({"message": "가족 초대가 거절되었습니다."}, status=status.HTTP_200_OK)

    return Response({"error": "잘못된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_event(request):
    # 현재 사용자로부터 가족을 가져옵니다.
    family = request.user.family

    # 일정 생성
    event = Event.objects.create(
        family=family,
        event_title=request.data['event_title'],
        event_content=request.data['event_content'],
        start_date=request.data['start_date'],
        end_date=request.data['end_date']
    )

    # 성공적으로 생성되었음을 응답합니다.
    return Response({"message": "일정이 추가되었습니다."}, status=status.HTTP_201_CREATED)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id, family=request.user.family)
        event.event_title = request.data['event_title']
        event.event_content = request.data['event_content']
        event.start_date = request.data['start_date']
        event.end_date = request.data['end_date']
        event.save()

        return Response({"message": "일정이 수정되었습니다."}, status=status.HTTP_200_OK)
    except Event.DoesNotExist:
        return Response({"error": "일정을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event(request, event_id):
    try:
        event = Event.objects.get(id=event_id, family=request.user.family)
        event.delete()
        return Response({"message": "일정이 삭제되었습니다."}, status=status.HTTP_200_OK)
    except Event.DoesNotExist:
        return Response({"error": "일정을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)



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



