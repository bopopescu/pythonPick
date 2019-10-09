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
    def get(self, request, topicName, pictureID):
        try:
            picture = Picture.objects.get(pictureID=pictureID)
        except:
            return JsonResponse({"status": 422, "message": "Can't get the object from database"}, safe=False, status=422)
        picture_list = serializers.serialize('json', [picture, ])
        return HttpResponse(picture_list, content_type="text/json-comment-filtered", status=201)

    def post(self, request, topicName, pictureID):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def put(self, request, topicName, pictureID):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def delete(self, request, topicName, pictureID):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)


class Pictures(APIView):
    #permission_classes = (IsAuthenticated,)
    def get(self, request, topicName):
        try:
            topic = Topic.objects.get(name=topicName)
            picture1 = Picture.objects.create_instance(
                "asfdasasdasdf.jpeg", 0, 15, 5, topic, "adaaasd")
            pictures = Picture.objects.filter(topicName=topicName)
            picture_list = serializers.serialize('json', pictures)
        except:
            return JsonResponse({"status": 422, "message": "Can't get the object from database"}, safe=False, status=422)
    
        return HttpResponse(picture_list, content_type="text/json-comment-filtered", status=201)

    def post(self, request, topicName):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def put(self, request, topicName):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def delete(self, request, topicName):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)
