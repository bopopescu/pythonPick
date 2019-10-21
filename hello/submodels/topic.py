from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class TopicManager(models.Manager):
    def create_instance(self, name, numberOfPhotos, tags, authorID):
        instance = self.create(name=name, numberOfPhotos=numberOfPhotos, tags=tags, authorID=authorID)
        # do something with the book
        return instance


class Topic(models.Model):
    topicID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    numberOfPhotos = models.IntegerField()
    authorID = models.ForeignKey(
        User,
        on_delete=models.CASCADE, default="0"
    )
    tags = models.CharField(max_length=100, default="photo")
    objects = TopicManager()
