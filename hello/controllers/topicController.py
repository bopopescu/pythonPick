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
from django.http import QueryDict
from django.contrib.auth.models import User


from hello.submodels.statusCodes import StatusCodes

class TopicController(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, topicID):
        try:
            topic = Topic.objects.get(topicID=topicID)
        except:
            return JsonResponse({"status": StatusCodes.FAILED_GET, "message": "Can't get topic object from database"}
            , safe=False, status=StatusCodes.FAILED_GET)
        topic_serialized = serializers.serialize('json', [topic])
        #removing json array clauses
        trimmed_result = topic_serialized[1:-1]
        return HttpResponse(trimmed_result, content_type="text/json-comment-filtered", status=StatusCodes.SUCCESFUL_GET)

    def put(self, request, topicID):
        try:
            tags = request.data.get("tags")
            Topic.objects.filter(topicID=topicID).update(tags=tags)
        except Exception as e:
             return JsonResponse({"status": StatusCodes.FAILED_PUT, "message": str(e)}
            , safe=False, status=StatusCodes.FAILED_PUT)

        return JsonResponse({"status": StatusCodes.SUCCESFUL_PUT, "message": "Object succesfully updated"}, safe=False, status=StatusCodes.SUCCESFUL_PUT)

    def delete(self, request, topicID):

        try:
            Topic.objects.get(topicID=topicID).delete()
        except Exception as e:
             return JsonResponse({"status": StatusCodes.FAILED_DELETE, "message": str(e)}
            , safe=False, status=StatusCodes.FAILED_DELETE)
        return JsonResponse({"status": StatusCodes.SUCCESFUL_DELETE, "message": "Successfully deleted"}, safe=False, status=StatusCodes.SUCCESFUL_DELETE)

class TopicsController(APIView):
   
    def get(self, request):
        
        try:
            topics = Topic.objects.all()
            topic_list = serializers.serialize('json', topics)
        except Exception as e:
            return JsonResponse({"status": StatusCodes.FAILED_GET, "message": str(e)}, safe=False, status=StatusCodes.FAILED_GET)
        
        return HttpResponse(topic_list, content_type="text/json-comment-filtered", status=StatusCodes.SUCCESFUL_GET)
    
    def post(self, request):

        try:
            username = request.user.username
            user = User.objects.get(username=username)
            topicName = request.data.get("topicName")
            tags = request.data.get("tags")
            topic = Topic.objects.create_instance(topicName, 0, tags, user)
        except Exception as e:
            return JsonResponse({"status": StatusCodes.FAILED_POST, "message": str(e)}
            , safe=False, status=StatusCodes.FAILED_POST)

        return JsonResponse({"status": StatusCodes.SUCCESFUL_POST, "message": "Object succesfully created"}, safe=False, status=StatusCodes.SUCCESFUL_POST)
