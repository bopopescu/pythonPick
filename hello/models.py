from django.db import models


class Comment(models.Model):
    commentID = models.CharField(max_length=20, primary_key=True)
    commentText = models.CharField(max_length=255)
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    authorID = models.CharField(max_length=20)

# Create your models here.
# Create your models here.
class Picture(models.Model):
    pictureUrl = models.CharField(max_length=100)
    pictureID = models.CharField(max_length=20, primary_key=True)
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    numberOfComments = models.IntegerField()
    authorID = models.CharField(max_length=20)
# Create your models here.


class TopicManager(models.Manager):
    def create_instance(self, name, numberOfPhotos):
        instance = self.create(name=name, numberOfPhotos=numberOfPhotos)
        # do something with the book
        return instance

class Topic(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    numberOfPhotos = models.IntegerField()
    objects = TopicManager()

        
