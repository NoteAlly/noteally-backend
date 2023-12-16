from django.db import models
from django.db import models
from storages.backends.s3 import S3Storage
from django.conf import settings


class StudyArea(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class University(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class User(models.Model):
    id = models.AutoField(primary_key=True) 
    sub = models.CharField(max_length=100, unique=True)  
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    premium = models.BooleanField(default=False)
    karma_score = models.IntegerField(default=0)
    study_areas = models.ManyToManyField(StudyArea) 
    description = models.TextField(blank=True)
    tutoring_services = models.BooleanField(default=False)
    profile_picture_name = models.CharField(max_length=100, blank=True)
    profile_pic_size = models.IntegerField(default=0)

    if settings.SETTINGS_MODULE == 'NoteAlly.production_settings':                
        profile_picture = models.FileField(upload_to='profile_pictures/', blank=True, storage=S3Storage(bucket_name='noteally-public-bucket', default_acl='public-read', querystring_auth=False))
    else:
        profile_picture = models.FileField(upload_to='profile_pictures/', blank=True)
    
    followers = models.ManyToManyField('self', through="Follower", through_fields=('follower', 'following'), symmetrical=False, related_name='following_users')
    
    
class Follower(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_set')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_set')

    class Meta:
        unique_together = ('follower', 'following')
    
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

    if settings.SETTINGS_MODULE == 'NoteAlly.production_settings':
        file = models.FileField(upload_to='materials/', blank=True, storage=S3Storage(bucket_name='noteally-bucket'))
    else:
        file = models.FileField(upload_to='materials/', blank=True)
    study_areas = models.ManyToManyField(StudyArea)
    total_likes = models.IntegerField(default=0)
    total_dislikes = models.IntegerField(default=0)
    total_downloads = models.IntegerField(default=0) 


class Download(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Material, on_delete=models.CASCADE)
    download_date = models.DateTimeField(auto_now_add=True)
    hidden = models.BooleanField(default=False) # If the user has hidden the download


class Like(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Material, on_delete=models.CASCADE)
    like = models.BooleanField()
