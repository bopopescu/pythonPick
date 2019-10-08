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
from hello.models.Topic import Topic


class TopicController(APIView):
    #permission_classes = (IsAuthenticated,)
    def get(self, request):
        return JsonResponse({status: 201, message: "Successful get"}, safe=False, status=201)
    def post(self, request):  
        return JsonResponse({status: 201, message: "Successfully created/post"}, safe=False, status=201)
    def put(self, request):
        return JsonResponse({status: 201, message: "Put successful"}, safe=False, status=201)
    def delete(self, request):
        return JsonResponse({status: 201, message: "Delete successful"}, safe=False, status=201)

class Topics(APIView):
    #permission_classes = (IsAuthenticated,)
    def get(self, request):
        topic1 = 
        thislist = ["apple", "banana", "cherry"]
        return JsonResponse({status: 201, message: "Forbidden"}, safe=False, status=201)

    def post(self, request):
        return JsonResponse({status: 403, message: "Forbidden"}, safe=False, status=403)

    def put(self, request):
        return JsonResponse({status: 403, message: "Forbidden"}, safe=False, status=403)

    def delete(self, request):
        return JsonResponse({status: 403, message: "Forbidden"}, safe=False, status=403)
        
