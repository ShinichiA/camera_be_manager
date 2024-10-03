import uuid
from enum import Enum

from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib import auth
from django.db.models import Q


def get_token():
    return str(uuid.uuid4())


class UserManager(BaseUserManager):

    def create_user(
            self, username, password=None, is_staff=False, is_active=True,
            **extra_fields):
        """Create a user instance with the given email and password."""
        # email = UserManager.normalize_email(email)
        extra_fields.pop('email', None)

        user = self.model(
            username=username, is_active=is_active, is_staff=is_staff,
            **extra_fields)
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        return self.create_user(
            username, password, is_staff=True, is_superuser=True, **extra_fields)

    def customers(self):
        return self.get_queryset().filter(
            Q(is_staff=False) | (Q(is_staff=True) & Q(orders__isnull=False)))

    def staff(self):
        return self.get_queryset().filter(is_staff=True)


# Create your models here.
class User(AbstractUser):
    name = models.CharField(max_length=255, blank=False)
    email = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255, unique=True, blank=False)
    password = models.CharField(max_length=255, blank=False)
    is_staff = models.BooleanField(default=False)
    token = models.UUIDField(default=get_token, editable=False, unique=True)
    is_active = models.BooleanField(default=True)
    note = models.TextField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)
    USERNAME_FIELD = 'username'

    objects = UserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'users'
        ordering = ('id',)


class Profile(models.Model):
    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER)
    birth_day = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class AccountUserRole(models.Model):
    class Role(Enum):
        SUPER_USER = 0
        OPERATION_ADMIN = 1
        OTHER = 2
        DEV = 3

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.IntegerField(choices=[(item.value, item.value) for item in Role], default=Role.OTHER.value)

    class Meta:
        db_table = 'account_user_role'
