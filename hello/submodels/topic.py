from django.db import models

class TopicManager(models.Manager):
    def create_instance(self, name, numberOfPhotos, tags):
        instance = self.create(name=name, numberOfPhotos=numberOfPhotos, tags=tags)
        # do something with the book
        return instance


class Topic(models.Model):
    topicID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    numberOfPhotos = models.IntegerField()
    tags = models.CharField(max_length=100, default="photo")
    objects = TopicManager()
