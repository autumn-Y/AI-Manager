from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

@csrf_exempt
# NUGU health check
def health(request):
    return JsonResponse({"message": "Ok"})

@csrf_exempt
def test(request):
    print("요청을 받았음")

    ctx = {}
    ctx["message"] = "example"

    respon = {
        "version": "2.0",
        "resultCode": "OK",
        "output":ctx,
    }

    return JsonResponse(respon)

@csrf_exempt
#answer.jansori
def alert_info(request):
    print("alert 요청 들어왔어요")
    # making the meassages
    alert_kind = "미세먼지주의보"
    lg_appliance = "공기청정기"
    
    ctx = {}
    ctx["messages"] = alert_kind + "가 있습니다. 마스크 착용 부탁드릴게요!"
    ctx["lghome"] = lg_appliance

    # nugu response set
    respon = {
        "version": "2.0",
        "resultCode": "OK",
        "output":ctx,
    }

    return JsonResponse(respon)

@csrf_exempt
#answer.jansori.lg
def lg_connect(request):
    print("요청이 들어왔어요")
    nugu_body = json.loads(request.body)
    lg_appliance = str(nugu_body.get("action").get("parameters").get("lghome").get('value'))
    print(lg_appliance)
    # making the meassages

    ctx = {}
    ctx["lgmessage"] = lg_appliance + "를 틀어드릴까요?"
    
    # nugu response set
    respon = {
        "version": "2.0",
        "resultCode": "OK",
        "output":ctx,
    }

    return JsonResponse(respon)    