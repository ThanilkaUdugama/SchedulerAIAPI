from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models



class UserManager(BaseUserManager):
    def create_user(self, email, full_name, country, timezone, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, full_name=full_name, country=country, timezone=timezone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, country, timezone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, full_name, country, timezone, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    profile = models.ImageField(upload_to='media/profiles/', null=True, blank=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    timezone = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['full_name', 'country', 'timezone']  

    def __str__(self):
        return self.email


class Notification(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    heading = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    notification = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.heading} - {self.account.email}"