from django.db import models


class StudyArea(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class User(models.Model):
    id = models.AutoField(primary_key=True)
    id_aws = models.IntegerField()
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    premium = models.BooleanField()
    university = models.CharField(max_length=100)
    karma_score = models.IntegerField()
    study_areas = models.ManyToManyField(StudyArea)
    description = models.TextField()
    tutoring_services = models.BooleanField()
    profile_picture_name = models.CharField(max_length=100)
    profile_picture_link = models.TextField()


class Resource(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField(default=0)
    upload_date = models.DateTimeField()
    university = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    file_link = models.TextField()
    study_areas = models.ManyToManyField(StudyArea)
    total_likes = models.IntegerField(default=0)
    total_dislikes = models.IntegerField(default=0)
    total_downloads = models.IntegerField(default=0)


class Download(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    download_date = models.DateTimeField()
    hidden = models.BooleanField(default=False) # If the user has hidden the download


class Like(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    like = models.BooleanField()
