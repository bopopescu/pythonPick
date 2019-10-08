from django.db import models

# Create your models here.


class Picture(models.Model):
    pictureUrl = models.CharField(max_length=100)
    pictureID = models.CharField(max_length=20, primary_key=True)
    likes = models.IntegerField()
    dislikes = models.IntegerField()
    numberOfComments = models.IntegerField()
    authorID = models.CharField(max_length=20)
