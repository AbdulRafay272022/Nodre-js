# myapp/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    admin=models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Prospect(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name_of_prospect = models.CharField(max_length=100)
    number_of_vehicles = models.IntegerField()
    existing_insurer = models.CharField(max_length=100, blank=True)
    decision_maker = models.CharField(max_length=100)
    decision_maker_phone = models.CharField(max_length=15)
    meeting_time_date = models.DateTimeField(null=True, blank=True)
    existing_rates = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name_of_prospect
