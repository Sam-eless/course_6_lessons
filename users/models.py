from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from django.db import models
from django.http import request
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from blog.models import NULLABLE
from config.settings import EMAIL_HOST_USER


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    first_name = models.CharField(max_length=100, verbose_name='имя')
    last_name = models.CharField(max_length=100, verbose_name='фамилия')
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    is_email_verified = models.BooleanField(verbose_name='email подтвержден', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

