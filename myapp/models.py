from django.db import models
from django.contrib.auth.models import User
from datetime import date

class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(unique=True, max_length=150)
    password = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'myapp_user'



class Question(models.Model):
    text = models.CharField(max_length=255)
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'myapp_question'

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, db_column='question_id')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_column='created_at')

    def __str__(self):
        return self.text

    class Meta:
        db_table = 'myapp_answer'