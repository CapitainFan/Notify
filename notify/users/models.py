from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password, avatar, first_name, last_name):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        if not password:
            raise ValueError('The Password field must be set')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            avatar=avatar,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, username, email, password, avatar, first_name, last_name):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            avatar=avatar,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password', 'avatar', 'first_name', 'last_name']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
