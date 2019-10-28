import re
import json
from django.http import HttpResponse
from datetime import datetime
from django.http import JsonResponse
from django.core import serializers

import traceback

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from hello.models import *
from django.core import serializers

from hello.submodels.statusCodes import StatusCodes

class PictureController(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, topicID, pictureID):
        try:
            picture = Picture.objects.get(pictureID=pictureID)
        except:
            return JsonResponse({"status": 422, "message": "Can't get the object from database"}, safe=False, status=StatusCodes.FAILED_GET)
        picture_list = serializers.serialize('json', [picture])
        trimmed_result = picture_list[1:-1]
        return HttpResponse(picture_list, content_type="text/json-comment-filtered", status=StatusCodes.SUCCESFUL_GET)
        

    def post(self, request, topicID, pictureID):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def put(self, request, topicID, pictureID):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def delete(self, request, topicID, pictureID):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)


class PicturesController(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, topicID):
        try:
            topic = Topic.objects.get(topicID=topicID)
            pictures = Picture.objects.filter(topicID=topicID)
            picture_list = serializers.serialize('json', pictures)
        except Exception as e:
            return JsonResponse({"status": StatusCodes.FAILED_GET, "message": str(e)}
                                , safe=False, status=StatusCodes.FAILED_GET)
        
        return HttpResponse(picture_list, content_type="text/json-comment-filtered", status=200)

    def post(self, request, topicID):
        try:
            pictureUrl = request.POST.get("pictureUrl")
            authorID = request.POST.get("authorID")
            user = request.user 
            topic = Topic.objects.get(topicID=topicID)
            #picture = Picture.objects.create_instance(pictureUrl = pictureUrl,
            #likes=0, dislikes= 0, numberOfComments =0, topicID = topic, authorID= authorID)
        except Exception as e:
            return JsonResponse({"status": 422, "message": str(e)}
            , safe=False, status=422)

        return JsonResponse({"status": 201, "message": "Object succesfully created"}, safe=False, status=201)
