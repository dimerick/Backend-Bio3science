from django.db import models
from django.contrib.gis.db import models as models_gis
from django.contrib.auth.models import UserManager, AbstractBaseUser

# Create your models here.

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [email]

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

class Degree(models.Model):
    name = models.CharField(max_length=100, unique=True)

class FieldsOfStudy(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    field_of_study = models.ForeignKey(FieldsOfStudy, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    websites = models.CharField(max_length=1000)
    university = models.CharField(max_length=200, unique=True)
    university_loc = models_gis.PointField()
