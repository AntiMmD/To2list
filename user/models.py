from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError
#I wanted to mess around with AbstractBaseUser for my user model

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        email = self.normalize_email(email)  
        username = username.lower()
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  
        user.save()  
        return user       
     
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, blank=True) 

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    def clean(self):
        self.username = self.username.lower()  
        if User.objects.filter(username__iexact=self.username).exclude(pk=self.pk).exists():   # I used exclude to ensure that updating a user instance doesn't accidentally flag the user’s own username as a duplicate.
            raise ValidationError("A user with this username already exists.")
        
    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)
