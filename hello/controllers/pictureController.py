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
    def get(self, request, topicID, pictureID):
        try:
            picture = Picture.objects.get(pictureID=pictureID)
        except:
            return JsonResponse({"status": 422, "message": "Can't get the object from database"}, safe=False, status=422)
        picture_list = serializers.serialize('json', [picture, ])
        return HttpResponse(picture_list, content_type="text/json-comment-filtered", status=201)

    def post(self, request, topicID, pictureID):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def put(self, request, topicID, pictureID):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def delete(self, request, topicID, pictureID):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)


class PicturesController(APIView):
    #permission_classes = (IsAuthenticated,)
    def get(self, request, topicID):
        try:
            topic = Topic.objects.get(topicID=topicID)
            pictures = Picture.objects.filter(topicID=topicID)
            picture_list = serializers.serialize('json', pictures)
        except Exception as e:
            return JsonResponse({"status": 422, "message": str(e)}
            , safe=False, status=422)
    
        return HttpResponse(picture_list, content_type="text/json-comment-filtered", status=200)

    def post(self, request, topicID):
        try:
            pictureUrl = request.POST.get("pictureUrl")
            authorID = request.POST.get("authorID")
            topic = Topic.objects.get(topicID=topicID)
            picture = Picture.objects.create_instance(pictureUrl = pictureUrl,
             likes=0, dislikes= 0, numberOfComments =0, topicID = topic, authorID= authorID)
        except Exception as e:
            return JsonResponse({"status": 422, "message": str(e)}
            , safe=False, status=422)

        return JsonResponse({"status": 201, "message": "Object succesfully created"}, safe=False, status=201)
