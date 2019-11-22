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
        
    def put(self, request, topicID, pictureID):
        try:
            rating = request.data.get("rating")
            previousPicture = Picture.objects.get(
                pictureID=pictureID)
            if rating == "like":
                previousRating = getattr(previousPicture, "likes")
                newRating = previousRating + 1
                Picture.objects.filter(
                    pictureID=pictureID).update(likes=newRating)
            elif rating == "dislike":
                previousRating = getattr(previousPicture, "dislikes")
                newRating = previousRating + 1
                Picture.objects.filter(
                    pictureID=pictureID).update(dislikes=newRating)
            else:
                return JsonResponse({"status": StatusCodes.FAILED_PUT, "message": "invalid rating"}, safe=False, status=StatusCodes.FAILED_PUT)
        except Exception as e:
             return JsonResponse({"status": StatusCodes.FAILED_PUT, "message": str(e)}
            , safe=False, status=StatusCodes.FAILED_PUT)

        return JsonResponse({"status": StatusCodes.SUCCESFUL_PUT, "message": "Picture rated"}, safe=False, status=StatusCodes.SUCCESFUL_PUT)

    def delete(self, request, topicID, pictureID):
        try:
            Picture.objects.get(pictureID=pictureID).delete()
        except Exception as e:
             return JsonResponse({"status": StatusCodes.FAILED_DELETE, "message": str(e)}, safe=False, status=StatusCodes.FAILED_DELETE)
        return JsonResponse({"status": StatusCodes.SUCCESFUL_DELETE, "message": "Successfully deleted"}, safe=False, status=StatusCodes.SUCCESFUL_DELETE)


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
            pictureUrl = request.data.get("pictureUrl")
            username = request.user.username
            user = User.objects.get(username=username)
            topic = Topic.objects.get(topicID=topicID)
            picture = Picture.objects.create_instance(pictureUrl = pictureUrl,
            likes=0, dislikes= 0, numberOfComments =0, topicID = topic, authorID=user)
        except Exception as e:
            return JsonResponse({"status": StatusCodes.FAILED_POST, "message": str(e)}, safe=False, status=StatusCodes.FAILED_POST)

        return JsonResponse({"status": StatusCodes.SUCCESFUL_POST, "message": "Object succesfully created"}, safe=False, status=StatusCodes.SUCCESFUL_POST)
