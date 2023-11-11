from typing import Any
from django.http import JsonResponse, HttpResponse
import json

from . import user

# Create your views here.
def login(request: Any):
    body_unicode = request.body.decode("utf-8")
    body_data = json.loads(body_unicode)

    r = user.getUser(body_data["username"])

    return JsonResponse({"User": f"{r}"})

def register(request: Any):
    body_unicode = request.body.decode("utf-8")
    body_data = json.loads(body_unicode)

    r = user.registerUser(body_data["username"], body_data["name"], body_data["password"])

    return r
