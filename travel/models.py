from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.http import request

from accounts.models import UserProfileInfo


class Photo(models.Model):
    user = models.ForeignKey(UserProfileInfo, default=1, on_delete=models.CASCADE)
    city = models.CharField(max_length=25)
    country = models.CharField(max_length=25)
    title = models.CharField(max_length=25)
    description = models.TextField()

    image_url = models.ImageField(upload_to='images')

    def __str__(self):
        return f"{self.title}: from {self.city}, {self.country}"


class Like(models.Model):
    photo = models.ForeignKey(to=Photo, default='', on_delete=models.CASCADE)
    user = models.ForeignKey(to=UserProfileInfo, default=1, on_delete=models.CASCADE)
    likes_count = ''

    def __str__(self):
        return f"{self.photo}"


class Comment(models.Model):
    photo = models.ForeignKey(to=Photo, default='', on_delete=models.CASCADE)
    user = models.ForeignKey(to=UserProfileInfo, default=1, on_delete=models.CASCADE)
    comment = models.TextField(max_length=256)

    def __str__(self):
        return f"{self.comment}"
