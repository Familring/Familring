from django.db import models

# Family 모델
class Family(models.Model):
    family_id = models.AutoField(primary_key=True)
    family_name = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)  # family 생성자

    def __str__(self):
        return self.family_name

# User 모델
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.set_password(password)  # 비밀번호 해싱
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

# Custom User model
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # 이 필드를 명시적으로 추가할 수 있음
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

# Furniture 모델 (메인페이지 스티커 관련)
class Furniture(models.Model):
    furniture_name = models.CharField(max_length=255)
    position_x = models.IntegerField()
    position_y = models.IntegerField()
    family = models.ForeignKey(Family, on_delete=models.CASCADE)

    def __str__(self):
        return self.furniture_name

# Album 모델
class Album(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    album_name = models.CharField(max_length=255)
    date = models.DateField()

    def __str__(self):
        return self.album_name

# Photo 모델 (앨범 내 사진)
class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    like_count = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo {self.id} in {self.album}"

# Comment 모델 (사진에 대한 댓글)
class Comment(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_content = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.photo}"

# Question 모델 (오늘의 질문)
class Question(models.Model):
    text = models.TextField()
    created_at_q = models.DateField(auto_now_add=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

# Answer 모델 (질문에 대한 답변)
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at_a = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Answer to {self.question}"

# Bucket List 모델
class BucketList(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    bucket_title = models.CharField(max_length=255)
    bucket_content = models.TextField()
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.bucket_title

# Calendar Event 모델 (캘린더 일정)
class Event(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    event_title = models.CharField(max_length=255)
    event_content = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.event_title
