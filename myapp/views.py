#import openai
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Question, Answer
from .serializers import UserSerializer, QuestionSerializer, AnswerSerializer
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, login as django_login
from datetime import date

# OpenAI API 키 설정
#openai.api_key = settings.OPENAI_API_KEY
'''
def generate_question():
    prompt = "Create a unique question for today."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=50
    )
    question_text = response.choices[0].text.strip()
    return question_text
'''
@api_view(['POST'])
def register(request):
    data = request.data
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
        request.session['username'] = user.username
        request.session.save()  # 세션 저장을 강제로 호출
        print(request.session.get('username'))
        return Response({'success': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def today_question(request):
    today = date.today()
    try:
        question = Question.objects.get(date=today)
    except Question.DoesNotExist:
        question_text = "no question"
        question = Question.objects.create(text=question_text, date=today)

    username = request.session.get('username')
    print(f"Session username: {username}")

    # user_id를 찾기 위해 추가
    user = User.objects.filter(username=username).first()
    answered = Answer.objects.filter(question=question, user=user).exists() if user else False

    serializer = QuestionSerializer(question)
    data = serializer.data
    data['answered'] = answered
    return Response(data)


@api_view(['GET', 'POST'])
def questions(request):
    if request.method == 'GET':
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def question_answers(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        answers = Answer.objects.filter(question=question)
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data.copy()
        data['question'] = question.id
        serializer = AnswerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
