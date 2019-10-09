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


class TopicController(APIView):
    #permission_classes = (IsAuthenticated,)
    def get(self, request, topicName):
        try:
            topic = Topic.objects.get(name=topicName)
        except:
            return JsonResponse({"status": 422, "message": "Can't get topic object from database"}
            , safe=False, status=422)
        topic_list = serializers.serialize('json', [topic, ])
        return HttpResponse(topic_list, content_type="text/json-comment-filtered", status=201)

    def post(self, request, topicName):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def put(self, request, topicName):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def delete(self, request, topicName):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

class Topics(APIView):
    #permission_classes = (IsAuthenticated,)
    def get(self, request):
        #topic1 = Topic.objects.create_instance("Cosmos", 0)
        #serialized_topic = serializers.serialize('json', topic1)
        topics = Topic.objects.all()
        topic_list = serializers.serialize('json', topics)
        return HttpResponse(topic_list, content_type="text/json-comment-filtered", status=201)

    def post(self, request):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def put(self, request):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)

    def delete(self, request):
        return JsonResponse({"status": 403, "message": "Forbidden"}, safe=False, status=403)
        
