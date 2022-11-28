from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

def get_congest(dest):
    # request argument : KEY, TYPE, SERVICE, START_INDEX, END_INDEX, AREA_NM
    # response : list_total_count, RESULT.CODE, RESULT.MESSAGE, AREA_NM, LIVE_PPLTAN_STTS, AREA_CONGEST_MSG

    apikey = '59496264636e796b37316473687768'
    startnum = 1
    endnum = 5


    df = pd.read_csv(r'nugu\views\seoul_main_50 places.csv')
    mask = (df['주변역']==dest)

    if mask.sum()==0:
        print("no such data")
        congest_lvl_f = "error"
        congest_msg_f = "error"
        return congest_msg_f, congest_lvl_f
        
    area_name = df.loc[mask, '장소명'].values[0]
    url1 = f'http://openapi.seoul.go.kr:8088/{apikey}/xml/citydata/{startnum}/{endnum}/{area_name}'

    result = requests.get(url1)
    soup = BeautifulSoup(result.text, "lxml")

    congest_lvl_f = soup.find('area_congest_lvl').get_text().strip()
    congest_msg_f = soup.find('area_congest_msg').get_text().strip()

    return congest_lvl_f, congest_msg_f

def special_date():
    # 어린이날 5/5
    if (datetime.today().month == "5") and (datetime.today().day == "5") :
        cmessage = " 오늘은 어린이날! 어디든 사람이 많을테니까 밖에 나가게 된다면 조심하기. 밖에 안나가는 것도 좋지."
    
    # 할로윈
    elif (datetime.today().month == "10") and (datetime.today().day == "5"):
        cmessage= " 오늘은 할로윈! 클럽 많은 홍대, 이태원, 강남 주요 동네를 간다면 정신 딱 붙들고 다녀. 밖에 안나가는 것도 좋지."

    # 크리스마스
    elif (datetime.today().month == "12") and (datetime.today().day == "25"):
        cmessage = " 와 벌써 크리스마스야. 올해가 얼마 남지 않았네. 크리스마스에 나가는 거 너무 좋지만 길거리에 사람이 정말 정말 많을거야. 조심해야해. 밖에 안나가는 것도 좋지."

    # 새해
    elif (datetime.today().month == "12") and (datetime.today().day == "31"):
        cmessage = " 새해 복 많이 받아! 오늘 보신각 갈거야? 일 년의 마지막날과 첫 날은 소중한 사람들과 함께 보내기!"
    
    else:
        cmessage = "normal"
    
    return cmessage

@csrf_exempt
def answer_congest(reqeust):
    nugu_body = json.loads(reqeust.body)
    # destination = nugu_body.get('action').get('parameters').get('DESTINATION').get('value')
    print(nugu_body)
    destination = nugu_body['action']['parameters']['DESTINATION']['value']
    print(destination)
    # subway_nm = "시청역"
    # place = "명동"
    congest_lvl, congest_msg = get_congest(destination)
    ctx={}

    if congest_msg == "error" :
        ctx['cmessage'] = "실시간 데이터에서 받아올 수 없는 지역이야. 미안해"
        
        # nugu response set
        respon = {
            "version": "2.1",
            "resultCode": "OK",
            "output":ctx,
        }
        return JsonResponse(respon) 

    ctx['cmessage'] = "현재 " + destination + "의 혼잡 정도는 " + congest_lvl + "(이)야. \"" + congest_msg + "\"라고 하네."

    special_msg = special_date()
    if special_msg != "normal":
        ctx['cmessage'] += special_msg

    print(ctx)
    # nugu response set
    respon = {
        "version": "2.1",
        "resultCode": "OK",
        "output":ctx,
    }

    return JsonResponse(respon) 