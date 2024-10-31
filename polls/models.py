import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    avatar = models.ImageField(upload_to='user_avatars', blank=False)

    def __str__(self):
        return self.username

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    question_desc_mini = models.TextField(default='краткого описания нет', blank=True)
    question_desc_full = models.TextField(default='описания нет', blank=True)
    pub_date = models.DateTimeField('date published')
    question_image = models.ImageField(upload_to='question_images', blank=True)
    expiration_date = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=7))

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - timezone.timedelta(days=1)

    def is_active(self):
        return self.expiration_date >= timezone.now()

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voted = models.BooleanField(default=False)

    def __str__(self):
        return f"'{self.user.username}' проголосовал за '{self.choice}' на вопрос '{self.question}'"