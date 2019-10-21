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


from hello.submodels.statusCodes import StatusCodes

class TopicController(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, topicID):
        try:
            topic = Topic.objects.get(topicID=topicID)
        except:
            return JsonResponse({"status": 422, "message": "Can't get topic object from database"}
            , safe=False, status=422)
        topic_serialized = serializers.serialize('json', [topic])
        #removing json array clauses
        trimmed_result = topic_serialized[1:-1]
        return HttpResponse(trimmed_result, content_type="text/json-comment-filtered", status=200)

    def put(self, request, topicID):
        try:
            tags = request.POST.get("tags")
            Topic.objects.filter(topicID=topicID).update(tags=tags)
        except Exception as e:
             return JsonResponse({"status": 422, "message": str(e)}
            , safe=False, status=422)

        return JsonResponse({"status": 222, "message": "Object succesfully updated"}, safe=False, status=222)

    def delete(self, request, topicID):

        try:
            Topic.objects.get(topicID=topicID).delete()
        except Exception as e:
             return JsonResponse({"status": 422, "message": str(e)}
            , safe=False, status=422)
        return JsonResponse({"status": 204, "message": "Successfully deleted"}, safe=False, status=204)

class TopicsController(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        
        topics = Topic.objects.all()
        topic_list = serializers.serialize('json', topics)
        return HttpResponse(topic_list, content_type="text/json-comment-filtered", status=200)

    
    def post(self, request):

        try:
            topicName = request.POST.get("topicName")
            tags = request.POST.get("tags")
            topic = Topic.objects.create_instance(topicName, 0, tags)
        except Exception as e:
            return JsonResponse({"status": 422, "message": str(e)}
            , safe=False, status=422)

        return JsonResponse({"status": 201, "message": "Object succesfully created"}, safe=False, status=201)