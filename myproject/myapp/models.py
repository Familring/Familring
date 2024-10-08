from django.db import models

# Family 모델
class Family(models.Model):
    family_id = models.AutoField(primary_key=True)
    family_name = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)  # family 생성자

    def __str__(self):
        return self.family_name

class FamilyList(models.Model):
    id = models.AutoField(primary_key=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    def __str__(self):
        return f"Family: {self.family.family_name}, User: {self.user.username}"

class FamilyRequest(models.Model):
    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='received_requests')
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    progress = models.CharField(max_length=50, default='진행중')  # 진행 상태 (진행중, 승인, 거절 등)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"FamilyRequest from {self.from_user.username} to {self.to_user.username}"

# User 모델
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

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
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=150)
    nickname = models.CharField(max_length=150, blank=True)  # nickname 필드 추가
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # 이 필드를 명시적으로 추가할 수 있음
    last_login = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


# Bucket List 모델
class BucketList(models.Model):
    bucket_id = models.AutoField(primary_key=True, default=1)
    family_id = models.ForeignKey(Family, on_delete=models.CASCADE)
    bucket_title = models.CharField(max_length=255)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.bucket_title


