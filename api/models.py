from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        # username = self.username
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, password, **extrafields):
        extrafields.setdefault('is_staff', True)
        extrafields.setdefault('is_superuser', True)
        extrafields.setdefault('is_active', True)

        if not extrafields.get('is_staff'):
            raise ValueError("SuperUser must have is_staff = True")
        
        if not extrafields.get('is_superuser'):
            raise ValueError("SuperUser must have is_superuser = True")
        
        return self.create_user(username, password, **extrafields)
        


class CustomUser(AbstractBaseUser):
    GENDER_CHOICES = (
        (1, 'male'),
        (2, 'female'),
        (3, 'other'),
    )
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128, null=True)
    phone_number = models.CharField(max_length=128)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gender = models.SmallIntegerField(choices=GENDER_CHOICES, null=True)
    age = models.SmallIntegerField(null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    objects = UserManager()

    def __str__(self):
        return self.username
    
    def has_module_perms(self, app_label):
        return True
    
    def has_perm(self, perm, obj=None):
        return True