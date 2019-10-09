from django.db import models
from hello.submodels.topic import *
from hello.submodels.picture import *

class Comment(models.Model):
    commentID = models.CharField(max_length=20, primary_key=True)
    commentText = models.CharField(max_length=255)
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    authorID = models.CharField(max_length=20)

# Create your models here
        
