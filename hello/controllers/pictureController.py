import re
import json
from django.http import HttpResponse
from datetime import datetime
from django.http import JsonResponse
from django.core import serializers

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from hello.models import *
from django.core import serializers


class PictureController(APIView):
    #permission_classes = (IsAuthenticated,)
    def get(self, request, topicName):
        try:
            topic = Topic.objects.get(name=topicName)
        except:
            return JsonResponse({"status": 422, "message": "Can't get topic object from database"}, safe=False, status=422)
        topic_list = serializers.serialize('json', [topic, ])
        return HttpResponse(topic_list, content_type="text/json-comment-filtered", status=201)

    def post(self, request, topicName):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def put(self, request, topicName):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def delete(self, request, topicName):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)


class Pictures(APIView):
    #permission_classes = (IsAuthenticated,)
    def get(self, request, topicName):
        topic = Topic.objects.get(name=topicName)

        picture1 = Picture.objects.create_instance("asfdasasdasdf.jpeg", 0, 15, 5, topic, "adaaasd")
        pictures = Picture.objects.all()
        picture_list = serializers.serialize('json', pictures)
        return HttpResponse(picture_list, content_type="text/json-comment-filtered", status=201)

    def post(self, request):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def put(self, request):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def delete(self, request):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)
