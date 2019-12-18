from django.db import models
from hello.submodels.topic import *
from django.conf import settings


class PictureManager(models.Manager):
    def create_instance(self, pictureUrl, likes, dislikes, numberOfComments, topicID, authorID, authorUsername, description):
        instance = self.create(pictureUrl = pictureUrl, likes=likes, dislikes=dislikes,
                               numberOfComments=numberOfComments, topicID=topicID, authorID=authorID, authorUsername=authorUsername, description=description)
        # do something with the book
        return instance

class Picture(models.Model):
    pictureUrl = models.CharField(max_length=100)
    pictureID = models.AutoField(primary_key=True)
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    numberOfComments = models.IntegerField()
    # foreign key in the
    topicID = models.ForeignKey(Topic, on_delete=models.CASCADE, default='UNSPECIFIED')
    authorID = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    authorUsername = models.CharField(max_length=255)
    description = models.CharField(max_length=100)
    objects = PictureManager()
    def get_model_fields(self):
        return self._meta.fields
