from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password, check_password

@api_view(['POST'])
def register(request):
    data = request.data.copy()  # 데이터를 복사하여 수정 가능하게 만듭니다.
    data['password'] = make_password(data['password'])
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
