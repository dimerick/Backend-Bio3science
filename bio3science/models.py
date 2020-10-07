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

class University(models.Model):
    name = models.CharField(max_length=200, unique=True)
    location = models_gis.PointField()

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, primary_key=True, on_delete=models.CASCADE)
    degree = models.ForeignKey(Degree, on_delete=models.CASCADE)
    field_of_study = models.ForeignKey(FieldsOfStudy, on_delete=models.CASCADE)
    description = models.CharField(max_length=1000)
    websites = models.CharField(max_length=1000)
    university = models.ForeignKey(University, on_delete=models.CASCADE)


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)

class Community(models.Model):
    name = models.CharField(max_length=200, unique=True)
    location = models_gis.PointField()

class ProjectXUniversityType(models.Model):
    name = models.CharField(max_length=200)


class ProjectXUniversity(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    project_x_university_type = models.ForeignKey(ProjectXUniversityType, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('project', 'university', 'project_x_university_type'))


class ProjectXCommunity(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('project', 'community'))



