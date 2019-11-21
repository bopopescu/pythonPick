from django.db import IntegrityError
from django.forms.models import model_to_dict
from django.test import TestCase
import string

from random import randint
from pytz import timezone

from django.conf import settings

from factory import Iterator
from factory import LazyAttribute
from factory import SubFactory
from factory import lazy_attribute
from factory.django import DjangoModelFactory, FileField
from factory.fuzzy import FuzzyText, FuzzyInteger
from faker import Factory as FakerFactory
from hello.submodels.topic import Topic
from hello.submodels.picture import Picture
from hello.submodels.comment import Comment
from django.db import models
import factory
import factory.django

from django.contrib.auth.models import User


faker = FakerFactory.create()

# models.py


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('email')
    password = factory.Faker('password')
    is_staff = True

class TopicFactory(DjangoModelFactory):
    class Meta:
        model = Topic

    name = LazyAttribute(lambda x: faker.text(max_nb_chars=100))
    numberOfPhotos = LazyAttribute(lambda o: randint(1, 100))
    authorID = SubFactory(UserFactory)
    tags = LazyAttribute(lambda x: faker.text(max_nb_chars=100))


class PictureFactory(DjangoModelFactory):
    class Meta:
        model = Picture

    pictureUrl = LazyAttribute(lambda x: faker.text(max_nb_chars=100))
    likes = LazyAttribute(lambda o: randint(1, 100))
    dislikes = LazyAttribute(lambda o: randint(1, 100))
    numberOfComments = LazyAttribute(lambda o: randint(1, 100))
    topicID = SubFactory(TopicFactory)
    authorID = SubFactory(UserFactory)


class CommentFactory(DjangoModelFactory):
    class Meta:
        model = Comment

    commentText = LazyAttribute(lambda x: faker.text(max_nb_chars=255))
    likes = LazyAttribute(lambda o: randint(1, 100))
    dislikes = LazyAttribute(lambda o: randint(1, 100))
    authorID = SubFactory(UserFactory)
    pictureID = SubFactory(PictureFactory)


class TestCaseTopic(TestCase):

    def test_create(self):
        """
        Test the creation of a Topic model using a factory
        """
        topic = TopicFactory.create()
        self.assertEqual(Topic.objects.count(), 1)

    def test_create_batch(self):
        """
        Test the creation of 5 Topic models using a factory
        """
        topics = TopicFactory.create_batch(5)
        self.assertEqual(Topic.objects.count(), 5)
        self.assertEqual(len(topics), 5)

    def test_attribute_count(self):
        """
        Test that all attributes of Topic server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        topic = TopicFactory.create()
        topic_dict = model_to_dict(topic)
        self.assertEqual(len(topic_dict.keys()), 5)

    def test_attribute_content(self):
        """
        Test that all attributes of Topic server have content. This test will break if an attributes name is changed.
        """
        topic = TopicFactory.create()
        self.assertIsNotNone(topic.topicID)
        self.assertIsNotNone(topic.name)
        self.assertIsNotNone(topic.numberOfPhotos)
        self.assertIsNotNone(topic.authorID)
        self.assertIsNotNone(topic.tags)

    def test_name_is_unique(self):
        """
        Tests attribute name of model Topic to see if the unique constraint works.
        This test should break if the unique attribute is changed.
        """
        topic = TopicFactory.create()
        topic_02 = TopicFactory.create()
        topic_02.name = topic.name
        try:
            topic_02.save()
            self.fail('Test should have raised and integrity error')
        except IntegrityError as e:
            self.assertEqual(str(e), '')  # FIXME This test is incomplete


class TestCasePicture(TestCase):

    def test_create(self):
        """
        Test the creation of a Picture model using a factory
        """
        picture = PictureFactory.create()
        self.assertEqual(Picture.objects.count(), 1)

    def test_create_batch(self):
        """
        Test the creation of 5 Picture models using a factory
        """
        pictures = PictureFactory.create_batch(5)
        self.assertEqual(Picture.objects.count(), 5)
        self.assertEqual(len(pictures), 5)

    def test_attribute_count(self):
        """
        Test that all attributes of Picture server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        picture = PictureFactory.create()
        picture_dict = model_to_dict(picture)
        self.assertEqual(len(picture_dict.keys()), 7)

    def test_attribute_content(self):
        """
        Test that all attributes of Picture server have content. This test will break if an attributes name is changed.
        """
        picture = PictureFactory.create()
        self.assertIsNotNone(picture.pictureUrl)
        self.assertIsNotNone(picture.pictureID)
        self.assertIsNotNone(picture.likes)
        self.assertIsNotNone(picture.dislikes)
        self.assertIsNotNone(picture.numberOfComments)
        self.assertIsNotNone(picture.topicID)
        self.assertIsNotNone(picture.authorID)


class TestCaseComment(TestCase):

    def test_create(self):
        """
        Test the creation of a Comment model using a factory
        """
        comment = CommentFactory.create()
        self.assertEqual(Comment.objects.count(), 1)

    def test_create_batch(self):
        """
        Test the creation of 5 Comment models using a factory
        """
        comments = CommentFactory.create_batch(5)
        self.assertEqual(Comment.objects.count(), 5)
        self.assertEqual(len(comments), 5)

    def test_attribute_count(self):
        """
        Test that all attributes of Comment server are counted. It will count the primary key and all editable attributes.
        This test should break if a new attribute is added.
        """
        comment = CommentFactory.create()
        comment_dict = model_to_dict(comment)
        self.assertEqual(len(comment_dict.keys()), 6)

    def test_attribute_content(self):
        """
        Test that all attributes of Comment server have content. This test will break if an attributes name is changed.
        """
        comment = CommentFactory.create()
        self.assertIsNotNone(comment.commentID)
        self.assertIsNotNone(comment.commentText)
        self.assertIsNotNone(comment.likes)
        self.assertIsNotNone(comment.dislikes)
        self.assertIsNotNone(comment.authorID)
        self.assertIsNotNone(comment.pictureID)
