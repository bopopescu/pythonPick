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

from hello.submodels.statusCodes import StatusCodes

from deprecated import deprecated


@deprecated(version='1.2.1', reason="You should use another function")
def pasenusFunkcija():
        print()

class CommentController(APIView):

    

    permission_classes = (IsAuthenticated,)
    def get(self, request, topicID, pictureID, commentID):
        try:
            comment = Comment.objects.get(commentID=commentID)
        except:
            return JsonResponse({"status": StatusCodes.FAILED_GET, "message": "Can't get the object from database"}, safe=False, status=StatusCodes.FAILED_GET)
        comment_list = serializers.serialize('json', [comment, ])  # ????

        pasenusFunkcija()
        return HttpResponse(comment_list, content_type="text/json-comment-filtered", status=StatusCodes.SUCCESFUL_GET)
        
    def put(self, request, topicID, pictureID, commentID):
        try:
            rating = request.data.get("rating")
            previousComment = Comment.objects.get(
                commentID=commentID)
            if rating == "like":
                previousRating = getattr(previousComment, "likes")
                newRating = previousRating + 1
                Comment.objects.filter(
                    commentID=commentID).update(likes=newRating)
            elif rating == "dislike":
                previousRating = getattr(previousComment, "dislikes")
                newRating = previousRating + 1
                Comment.objects.filter(
                    pictureID=pictureID).update(dislikes=newRating)
            else:
                return JsonResponse({"status": StatusCodes.FAILED_PUT, "message": "invalid rating"}, safe=False, status=StatusCodes.FAILED_PUT)
        except Exception as e:
             return JsonResponse({"status": StatusCodes.FAILED_PUT, "message": str(e)}, safe=False, status=StatusCodes.FAILED_PUT)

        return JsonResponse({"status": StatusCodes.SUCCESFUL_PUT, "message": "Picture rated"}, safe=False, status=StatusCodes.SUCCESFUL_PUT)

    def delete(self, request, topicID, pictureID, commentID):
        try:
            Comment.objects.get(commentID=commentID).delete()
        except Exception as e:
             return JsonResponse({"status": StatusCodes.FAILED_DELETE, "message": str(e)}, safe=False, status=StatusCodes.FAILED_DELETE)
        return JsonResponse({"status": StatusCodes.SUCCESFUL_DELETE, "message": "Successfully deleted"}, safe=False, status=StatusCodes.SUCCESFUL_DELETE)


class Comments(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, topicID, pictureID):
        try:
            comments = Comment.objects.filter(pictureID=pictureID)
            comments_list = serializers.serialize('json', comments)
        except Exception as e:
            return JsonResponse({"status": StatusCodes.FAILED_GET, "message": str(e)}
                                , safe=False, status=StatusCodes.FAILED_GET)
        if comments:
            return HttpResponse(comments_list, content_type="text/json-comment-filtered", status=200)
        else:
            return JsonResponse({"status": StatusCodes.FAILED_GET, "message": "found no records"}, safe=False, status=StatusCodes.FAILED_GET)
        

    def post(self, request, topicID, pictureID):
        try:
            commentText = request.data.get("commentText")
            username = request.user.username
            user = User.objects.get(username=username)
            picture = Picture.objects.get(pictureID=pictureID)
            comment = Comment.objects.create_instance(commentText=commentText,
                                                      likes=0, dislikes=0, authorID=user, pictureID=picture)

            previousRating = getattr(picture, "numberOfComments")
            newRating = previousRating + 1
            Picture.objects.filter(
                pictureID=pictureID).update(numberOfComments=newRating)
        except Exception as e:
            return JsonResponse({"status": StatusCodes.FAILED_POST, "message": str(e)}, safe=False, status=StatusCodes.FAILED_POST)

        return JsonResponse({"status": StatusCodes.SUCCESFUL_POST, "message": "Object succesfully created"}, safe=False, status=StatusCodes.SUCCESFUL_POST)
