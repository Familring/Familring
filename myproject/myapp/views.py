from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, BucketList, Family
from .serializers import UserSerializer, BucketListSerializer
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



