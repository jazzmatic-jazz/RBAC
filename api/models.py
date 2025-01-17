from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .choices import ROLE
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    '''
        Custom User Model stores the details of the user
        - email (Email)
        - name (char)
        - username (char)
        - role (char, choices)
        - is_deleted (Bool)

        Username : for login field and register field
    '''
    
    email = models.EmailField(max_length=254, unique=True, null=False, blank=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    role = models.CharField(max_length=2, choices=ROLE, default="EM")
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        return self.email


class Resource(models.Model):
    '''
        Resource table stores the resources created by Admin and Manager
        - created_by (FK)
        - name (char)
        - description (text)
        - created_at (DT)
        - updated_at (DT)
        - is_deleted (Bool)

        Returns: name and created_by
    '''

    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.created_by}"


