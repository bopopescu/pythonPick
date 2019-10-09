from django.db import models

class TopicManager(models.Manager):
    def create_instance(self, name, numberOfPhotos):
        instance = self.create(name=name, numberOfPhotos=numberOfPhotos)
        # do something with the book
        return instance


class Topic(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    numberOfPhotos = models.IntegerField()
    objects = TopicManager()
