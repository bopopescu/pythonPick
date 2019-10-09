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


class CommentController(APIView):
    #permission_classes = (IsAuthenticated,)
    def get(self, request, topicName, pictureID, commentID):
        try:
            comment = Comment.objects.get(commentID=commentID)
        except:
            return JsonResponse({"status": 422, "message": "Can't get the object from database"}, safe=False, status=422)
        comment_list = serializers.serialize('json', [comment, ])
        return HttpResponse(comment_list, content_type="text/json-comment-filtered", status=201)

    def post(self, request, topicName, pictureID, commentID):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def put(self, request, topicName, pictureID, commentID):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def delete(self, request, topicName, pictureID, commentID):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)


class Comments(APIView):
    #permission_classes = (IsAuthenticated,)
    def get(self, request, topicName, pictureID):
        #try:
            picture = Picture.objects.get(pictureID=pictureID)
            comment1 = Comment.objects.create_instance(
                "Labai grazi foto", 0, 15, "aasdasd", picture)
            comments = Comment.objects.filter(pictureID=pictureID)
            comment_list = serializers.serialize('json', comments)
        #except:
            #return JsonResponse({"status": 422, "message": "Can't get the object from database"}, safe=False, status=422)

            return HttpResponse(comment_list, content_type="text/json-comment-filtered", status=201)

    def post(self, request, topicName, pictureID):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def put(self, request, topicName, pictureID):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def delete(self, request, topicName, pictureID):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)
