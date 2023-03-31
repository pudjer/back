from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    language = models.ManyToManyField('Language', related_name='user_languages', blank=True)


class Language(models.Model):
    name = models.CharField(max_length=15, primary_key=True)

class Tag(models.Model):
    name = models.CharField(max_length=31, primary_key=True)