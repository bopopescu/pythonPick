from django.db import models

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    numberOfPhotos = models.IntegerField()

    @classmethod
    def create(cls, name, numberOfPhotos):
        instance = cls(name=name, numberOfPhotos=numberOfPhotos)
        # do something with the book
        return instance


class TopicManager(models.Manager):
    def create_instance(self, name, numberOfPhotos):
        instance = self.create(name=name, numberOfPhotos=numberOfPhotos)
        # do something with the book
        return instance
