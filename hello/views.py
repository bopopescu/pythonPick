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

from fastapi import FastAPI, HTTPException


def home(request):
    return JsonResponse({'status': 'false', 'message': "message"}, status=500)


def hello_there(request, name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return JsonResponse(content, safe=False)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):

        if IsAuthenticated:
            helloUser = "hello authenticated user"
            return JsonResponse(helloUser, safe=False)
        else:
            helloUser = "hello unauthenticated user"
            return JsonResponse(helloUser, safe=False)


    def post(self, request):

        if IsAuthenticated:
            helloUser = "hello authenticated user"
            return JsonResponse(helloUser, safe=False)
        else:
            helloUser = "hello unauthenticated user"
            return JsonResponse(helloUser, safe=False)
