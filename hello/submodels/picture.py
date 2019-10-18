from django.db import models
from hello.submodels.topic import *

class PictureManager(models.Manager):
    def create_instance(self, pictureUrl, likes, dislikes, numberOfComments,topicID, authorID):
        instance = self.create(pictureUrl = pictureUrl, likes=likes, dislikes=dislikes,
                               numberOfComments=numberOfComments, topicID = topicID, authorID=authorID)
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
    authorID = models.CharField(max_length=20)
    objects = PictureManager()
