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

class JwtTests(TestCase):

    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='user', email='jacob@…', password='pass')
        Topic.objects.create_instance("Cars", 0, "bwm audi", self.user)
        Topic.objects.create_instance("Animals", 0, "dogs kitten", self.user)

    def test_obtain_token(self):
        response = self.client.post(
            '/api/token/', {'username': 'user', 'password': 'pass'}, **{'wsgi.url_scheme': 'https'})
        self.assertEquals(response.status_code, 200)
        json_data = json.dumps(response.data)
        assert 'access' in json_data
        assert 'refresh' in json_data
        
    def test_get_Topics_with_token(self):
        response = self.client.post(
            '/api/token/', {'username': 'user', 'password': 'pass'}, **{'wsgi.url_scheme': 'https'})
        self.assertEquals(response.status_code, 200)
        json_data = json.dumps(response.data)
        assert 'access' in json_data
        assert 'refresh' in json_data
        json_variables = json.loads(json_data)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=' Bearer ' + json_variables['access'])

        response = client.get('/api/topics/', **
                              {'wsgi.url_scheme': 'https'})

        self.assertEquals(response.status_code, 200)
