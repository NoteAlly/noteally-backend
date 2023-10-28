from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import binascii
import datetime
import os
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class TTDToken(models.Model):
    key = models.CharField(_("Key"), max_length=40, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    ttd = models.DateTimeField(_("Time to die"))

    class Meta:
        # Work around for a bug in Django:
        # https://code.djangoproject.com/ticket/19422
        #
        # Also see corresponding ticket:
        # https://github.com/encode/django-rest-framework/issues/705
        abstract = 'rest_framework.authtoken' not in settings.INSTALLED_APPS
        verbose_name = _("Token")
        verbose_name_plural = _("Tokens")

    def save(self, *args, **kwargs):
        if not self.key or not self.ttd:
            self.key = self.generate_key()
            self.ttd = datetime.datetime.utcnow() + settings.TOKEN_EXPIRE_TIME
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key

class StudyArea(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class University(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')  

        user = self.model(
            email=email
        ) 
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email), 
            password=password,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, email):
        return self.get(email=email)
 
class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True) 
    id_aws = models.IntegerField()  
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    premium = models.BooleanField()
    university = models.ForeignKey(University, on_delete=models.DO_NOTHING)
    karma_score = models.IntegerField()
    study_areas = models.ManyToManyField(StudyArea)
    description = models.TextField()
    tutoring_services = models.BooleanField()
    profile_picture_name = models.CharField(max_length=100)
    profile_picture_link = models.TextField()
    
    USERNAME_FIELD = 'email'
    
    objects = CustomUserManager() 
    
class Material(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField(default=0)
    upload_date = models.DateTimeField(auto_now_add=True)
    university = models.ForeignKey(University, on_delete=models.DO_NOTHING)
    file_name = models.CharField(max_length=100, blank=True)
    file_size = models.IntegerField(default=0)
    file = models.FileField(upload_to='materials/', blank=True)
    study_areas = models.ManyToManyField(StudyArea)
    total_likes = models.IntegerField(default=0)
    total_dislikes = models.IntegerField(default=0)
    total_downloads = models.IntegerField(default=0) 
    
  

class Download(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Material, on_delete=models.CASCADE)
    download_date = models.DateTimeField()
    hidden = models.BooleanField(default=False) # If the user has hidden the download


class Like(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Material, on_delete=models.CASCADE)
    like = models.BooleanField()
