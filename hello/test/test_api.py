from django.test import TestCase
from django.test import Client
import json
import os

from django.http import HttpRequest
from django.urls import reverse
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser, User
from rest_framework.test import APIRequestFactory
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from django.db import models
from hello.submodels.topic import *
from hello.submodels.picture import *
from hello.submodels.comment import *

from hello.submodels.statusCodes import StatusCodes


class UnauthorizedAPICalls(TestCase):

    def test_get_Topic_List_Without_Access_Token_status_code(self):
        response = self.client.get(
            '/api/topics/', **{'wsgi.url_scheme': 'https'})
        self.assertEquals(response.status_code, 401)

    def test_get_Topic_By_Id_Without_Access_Token_status_code(self):
        response = self.client.get(
            '/api/topics/1/', **{'wsgi.url_scheme': 'https'})
        self.assertEquals(response.status_code, 401)

    def test_get_Pictures_List_Without_Access_Token_status_code(self):
        response = self.client.get(
            '/api/topics/1/pictures/', **{'wsgi.url_scheme': 'https'})
        self.assertEquals(response.status_code, 401)

    def test_get_Picture_By_Id_Without_Access_Token_status_code(self):
        response = self.client.get(
            '/api/topics/1/pictures/1/', **{'wsgi.url_scheme': 'https'})
        self.assertEquals(response.status_code, 401)

    def test_get_Comments_List_Without_Access_Token_status_code(self):
        response = self.client.get(
            '/api/topics/1/pictures/1/comments/', **{'wsgi.url_scheme': 'https'})
        self.assertEquals(response.status_code, 401)

    def test_get_Comment_By_Id_Without_Access_Token_status_code(self):
        response = self.client.get(
            '/api/topics/1/pictures/1/comments/1/', **{'wsgi.url_scheme': 'https'})
        self.assertEquals(response.status_code, 401)


class AuthorizedApiCallsWithNoRecordsInDatabase(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='user', email='jacob@…', password='pass')

        response = self.client.post(
            '/api/token/', {'username': 'user', 'password': 'pass'}, **{'wsgi.url_scheme': 'https'})
        self.assertEquals(response.status_code, 200)
        json_data = json.dumps(response.data)
        assert 'access' in json_data
        assert 'refresh' in json_data

        json_variables = json.loads(json_data)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=' Bearer ' +
                                json_variables['access'])

    def test_get_Topics_with_token(self):
        response = self.client.get('/api/topics/', **
                                   {'wsgi.url_scheme': 'https'})

        self.assertEquals(response.status_code, 200)


    def test_get_Topic_by_id_with_token(self):
        response = self.client.get('/api/topics/1/', **
                                   {'wsgi.url_scheme': 'https'})

        self.assertEquals(response.status_code, StatusCodes.FAILED_GET)

    def test_get_Pictures_with_token(self):
        response = self.client.get('/api/topics/1/pictures/', **
                                   {'wsgi.url_scheme': 'https'})

        self.assertEquals(response.status_code, StatusCodes.FAILED_GET)

    def test_get_Picture_by_id_with_token(self):
        response = self.client.get('/api/topics/1/pictures/1/', **
                                   {'wsgi.url_scheme': 'https'})

        self.assertEquals(response.status_code, StatusCodes.FAILED_GET)

    def test_get_Comments_with_token(self):
        response = self.client.get('/api/topics/1/pictures/9999/comments/', **
                                   {'wsgi.url_scheme': 'https'})

        self.assertEquals(response.status_code, StatusCodes.FAILED_GET)

    def test_get_Comment_by_id_with_token(self):
        response = self.client.get('/api/topics/1/pictures/1/comments/1/', **
                                   {'wsgi.url_scheme': 'https'})

        self.assertEquals(response.status_code, StatusCodes.FAILED_GET)


class AuthorizedApiCalls(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='user', email='jacob@…', password='pass')

        topic0 = Topic.objects.create_instance(
            "Cars", 0, "bwm audi", self.user)
        topic1 = Topic.objects.create_instance(
            "Animals", 0, "dogs kitten", self.user)
        picture0 = Picture.objects.create_instance(
            "ajoiodjasd.jpeg", 0, 0, 0, topic0, self.user)
        picture1 = Picture.objects.create_instance(
            "ajoiasdasdasd.jpeg", 0, 0, 0, topic1, self.user)
        picture2 = Picture.objects.create_instance(
            "ajoiasdafdgsdasd.jpeg", 0, 0, 0, topic0, self.user)
        Comment.objects.create_instance(
            "Very nice picture", 0, 0, self.user, picture0)

        response = self.client.post(
            '/api/token/', {'username': 'user', 'password': 'pass'}, **{'wsgi.url_scheme': 'https'})
        self.assertEquals(response.status_code, 200)
        json_data = json.dumps(response.data)
        assert 'access' in json_data
        assert 'refresh' in json_data

        json_variables = json.loads(json_data)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=' Bearer ' +
                                json_variables['access'])

   

    def test_get_Topics_with_token(self):
        response = self.client.get('/api/topics/', **
                                   {'wsgi.url_scheme': 'https'})

        self.assertEquals(response.status_code, 200)

    def test_correct_post_create_Topic_with_token(self):
        topicCount = Topic.objects.count()
        response = self.client.post('/api/topics/', {'topicName': 'birds', 'tags': 'sparrow chiken'}, **
                                   {'wsgi.url_scheme': 'https'})

        self.assertEqual(Topic.objects.count(), topicCount+1)
        self.assertEquals(response.status_code, StatusCodes.SUCCESFUL_POST)


    def test_incorrect_post_create_Topic_with_token(self):
        topicCount = Topic.objects.count()
        response = self.client.post('/api/topics/', {'topicNameaa': 'birds', 'tags': 'sparrow chiken'}, **
                                    {'wsgi.url_scheme': 'https'})
        updatedCount = topicCount + 1
        self.assertEquals(response.status_code, StatusCodes.FAILED_POST)
        self.assertNotEqual(topicCount, updatedCount)


    def test_correct_put_Topic_with_token(self):
        topicCount = Topic.objects.count()
        response = self.client.put('/api/topics/1/', {'topicName': 'birds', 'tags': 'chiko koko achiken'}, **
                                    {'wsgi.url_scheme': 'https'})

        obj = Topic.objects.get(pk=1)
        field_name = 'tags'
        field_value = getattr(obj, field_name)

        self.assertEquals(response.status_code, StatusCodes.SUCCESFUL_PUT)
        self.assertEqual(field_value, 'chiko koko achiken')

    def test_incorrect_put_Topic_with_token(self):
        response = self.client.put('/api/topics/1/', {'topicNamess': 'birds', 'tagss': 'aaaachiko koko achiken'}, **
                                   {'wsgi.url_scheme': 'https'})

        self.assertEquals(response.status_code, StatusCodes.FAILED_PUT)

    def test_correct_get_Topic_by_id_with_token(self):
        response = self.client.get('/api/topics/1/', **
                                   {'wsgi.url_scheme': 'https'})

        self.assertEquals(response.status_code, 200)

    def test_incorrect_get_Topic_by_id_with_token(self):
        response = self.client.get('/api/topics/9999/', **
                                   {'wsgi.url_scheme': 'https'})

        self.assertEquals(response.status_code, StatusCodes.FAILED_GET)

    def test_correct_delete_Topic_with_token(self):
        topicCount = Topic.objects.count()
        response = self.client.delete('/api/topics/1/', **
                                   {'wsgi.url_scheme': 'https'})

        self.assertEquals(response.status_code, StatusCodes.SUCCESFUL_DELETE)
        self.assertEqual(Topic.objects.count(), topicCount-1)

    def test_incorrect_delete_Topic_with_token(self):
        topicCount = Topic.objects.count()
        response = self.client.delete('/api/topics/9999/', **
                                      {'wsgi.url_scheme': 'https'})

        self.assertEquals(response.status_code, StatusCodes.FAILED_DELETE)
        self.assertEqual(Topic.objects.count(), topicCount)

    def test_get_Pictures_with_token(self):
        response = self.client.get('/api/topics/1/pictures/', **
                                   {'wsgi.url_scheme': 'https'})

        self.assertEquals(response.status_code, 200)

    def test_get_Pictures_with_token(self):
        response = self.client.get('/api/topics/1/pictures/1/', **
                                   {'wsgi.url_scheme': 'https'})

        self.assertEquals(response.status_code, 200)

    def test_get_Comments_with_token(self):
        response = self.client.get('/api/topics/1/pictures/1/comments/', **
                                   {'wsgi.url_scheme': 'https'})

        self.assertEquals(response.status_code, 200)

    def test_get_Comment_by_id_with_token(self):
        response = self.client.get('/api/topics/1/pictures/1/comments/1/', **
                                   {'wsgi.url_scheme': 'https'})

        self.assertEquals(response.status_code, 200)
