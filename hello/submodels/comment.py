from django.db import models
from hello.submodels.topic import *
from hello.submodels.picture import *


class CommentManager(models.Manager):
    def create_instance(self, commentText, likes, dislikes, authorID):
        instance = self.create(commentText=commentText, likes=likes, dislikes=dislikes, authorID=authorID)
        # do something with the book
        return instance

class Comment(models.Model):
    commentID = models.AutoField(primary_key=True)
    commentText = models.CharField(max_length=255)
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    authorID = models.CharField(max_length=20)

    pictureID = models.ForeignKey(
        Picture, on_delete=models.CASCADE, default=0)
    objects = CommentManager()

