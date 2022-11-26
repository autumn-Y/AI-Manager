from django.shortcuts import render
from .models import Members
from django.views import View
from django.http import JsonResponse
from django.http import HttpResponse
import json

# Create your views here.


def index(request):
    return HttpResponse("You're at the support index")


class SignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            Members.objects.create(name=data["user_name"], id=data["user_id"],
                                   pw=data["user_pw"], location=data["user_location"])

            return JsonResponse({"message": "created"}, status=200)
        except KeyError:
            return JsonResponse({"message": "KEY_ERROR"}, status=400)


class Identify(View):
    def identify(self, request, *args, **kwargs):
        request_id = request.Get.get('id', None)
        request_pw = request.Get.get('pw', None)

        user = Members.objects.get(id=request_id)
        if user.pw != request_pw:
            return JsonResponse({"message": False}, status=404)
        else:
            return JsonResponse({"message": True}, status=200)







