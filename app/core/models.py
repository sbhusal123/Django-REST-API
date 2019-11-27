from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                                        PermissionsMixin

"""
PermissionMixins: https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#django.contrib.auth.models.PermissionsMixin
AbstractBaseUser: https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser
BaseUserManager: https://docs.djangoproject.com/en/2.1/topics/auth/customizing/#django.contrib.auth.models.BaseUserManager
Abstract base classes: https://docs.djangoproject.com/en/2.2/topics/db/models/#abstract-base-classes
Writing a manager for a custom user model: https://docs.djangoproject.com/en/2.2/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
""" # noqa


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self.db)  # to support the database query
        return user

    def create_superuser(self, email, password):
        """Creates and saves a new user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'email'