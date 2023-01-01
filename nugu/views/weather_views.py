from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

# -------------get data-----HEO YUNSEO-------------------------------------
import requests
import datetime
import pandas as pd
import bs4
import schedule

base_date, base_time, standard_date = '', '', ''
locationX = '55'                    #여기엔 나중에 사용자 위치 정보 받아서 넣어야됨
locationY = '127'                   #여기엔 나중에 사용자 위치 정보 받아서 넣어야됨
location = '성동구'
weather, weather_msg = {}, {}       #NUGU한테 줄 때 편하라고 딕셔너리 타입으로 변수들 저장


def re_time():
    now = datetime.datetime.now()
    d = now.date()
    global base_date
    base_date = d.strftime('%Y%m%d')
    t = now.time()
    global base_time
    base_time = t.strftime('%H%M')
    global standard_date
    standard_date = str(int(base_date)-1)


def weather_data():     #최저기온, 최고기온, 습도, 강수 확률 관련
    hot_msg, cold_msg, reh_msg, rain_msg = 0, 0, 0, 0  # 0일때는 특수 메시지 필요 없는것, 1일때는 필요한것
    re_time()
    url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
    servicekey = 'XZ9kxxXefiUI3gSeGe0%2FRtOtOSjRP%2B7pPEiUe6kYZmip%2FMAQkHJCLmEySAUSOnQYihwtcMF%2BGRAexUoiGaw%2BnA%3D%3D'
    url = (url + '?serviceKey=' + servicekey +
           '&pageNo=1&numOfRows=289&dataType=XML'
           + '&base_date=' + standard_date + '&base_time=2359'
           + '&nx=' + locationX + '&ny=' + locationY)
    res = requests.get(url)
    content = res.text

    xml_obj = bs4.BeautifulSoup(content, 'lxml-xml')
    rows = xml_obj.findAll('item')

    row_list = []
    name_list = []
    value_list = []

    for i in range(0, len(rows)):
        columns = rows[i].find_all()
        for j in range(0, len(columns)):
            if i == 0:
                name_list.append(columns[j].name)
            value_list.append(columns[j].text)
        row_list.append(value_list)
        value_list = []

    weather_df = pd.DataFrame(row_list, columns=name_list)

    weather_df.drop('baseDate', axis=1, inplace=True)
    weather_df.drop('baseTime', axis=1, inplace=True)
    weather_df.drop('nx', axis=1, inplace=True)
    weather_df.drop('ny', axis=1, inplace=True)

    # 데이터를 '오전 5시~ 다음날 오전 5시'를 기준으로 받아오는데, 하루 최고, 최저 온도가 오전 0시~5시 사이에 존재하는 경우에 에러 발생
    # 그래서 최저기온 데이터가 없을 경우를 상정해야함(12시~12시 기준으로 하면 api 받아오는거 자체에서 에러남-5시에 발표 시작?그런 느낌,,,)
    # 11.17 수정) 그냥 시간 기준을 밤11시~다음 날 밤 11시로 바꾸기로 했음

    tmx = weather_df[weather_df['category'] == 'TMX']
    tmn = weather_df[weather_df['category'] == 'TMN']

    if len(tmx) == 0:
        tmx = '예상 최고 기온 데이터를 받아오지 못하였습니다.'
    else:
        tmx = weather_df[weather_df['category'] == 'TMX'].iloc[0]['fcstValue']
        tmx = float(tmx)
        if tmx >= 32:
            hot_msg = 1     #폭염 관련 메세지 넣기

    if len(tmn) == 0:
        tmn = '예상 최저 기온 데이터를 받아오지 못하였습니다.'
    else:
        tmn = weather_df[weather_df['category'] == 'TMN'].iloc[0]['fcstValue']
        tmn = float(tmn)
        if tmn <= -5:
            cold_msg = 1     #한파 관련 메세지 넣기

    reh_df = weather_df[weather_df['category'] == 'REH']
    reh_df = reh_df.astype({'fcstValue':float})
    reh = reh_df['fcstValue'].mean()
    reh = round(reh, 2)
    if reh < 35:
        reh_msg = 1     #실효습도가 35% 이하일때는 건조주의보 -> 관련 메세지 넣기


    #일 평균 강수확률 = 강수확률 10프로 이상일 시간대만 모아서 평균내기
    #강수확률만 사용할거니까 카테고리 pop인것만 남기고, 밸류 데이터타입 int로 바꿈(원래 오브젝트)
    weather_df = weather_df[weather_df['category'] == 'POP']
    weather_df['fcstValue'] = weather_df['fcstValue'].astype(int)

    weather_df = weather_df[weather_df['fcstValue'] >= 10]
    pop = weather_df['fcstValue'].mean()
    pop = round(pop, 2)

    #강수 확률 40% 이상인 시간대 있으면 비온다고 말해주기
    weather_df = weather_df[weather_df['fcstValue'] >= 40]
    if len(weather_df) != 0:
        rain_msg = 1        #비 올 확률 40% 이상이라고 알려주는 메세지 필요

    global weather, weather_msg
    weather = {'최고기온': tmx, '최저기온': tmn, '평균습도': reh, '강수확률': pop}
    weather_msg = {'폭염': hot_msg, '한파': cold_msg, '건조주의보': reh_msg, '강수메세지': rain_msg}

def fine_dust():
    fine_msg = 0
    re_time()
    servicekey = 'XZ9kxxXefiUI3gSeGe0%2FRtOtOSjRP%2B7pPEiUe6kYZmip%2FMAQkHJCLmEySAUSOnQYihwtcMF%2BGRAexUoiGaw%2BnA%3D%3D'
    url = ('http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?serviceKey=' + servicekey
           + '&returnType=xml&numOfRows=100&pageNo=1&sidoName=%EC%84%9C%EC%9A%B8&ver=1.0')
    res = requests.get(url)
    content = res.text

    xml_obj = bs4.BeautifulSoup(content, 'lxml-xml')
    rows = xml_obj.findAll('item')

    row_list = []
    name_list = []
    value_list = []

    for i in range(0, len(rows)):
        columns = rows[i].find_all()
        for j in range(0, len(columns)):
            if i == 0:
                name_list.append(columns[j].name)
            value_list.append(columns[j].text)
        row_list.append(value_list)
        value_list = []

    dust_df = pd.DataFrame(row_list, columns=name_list)
    dust_df = dust_df[['pm10Grade', 'pm10Value', 'pm25Grade', 'stationName']]

    fine_msg = dust_df[dust_df['stationName'] == '성동구'].iloc[0]['pm10Grade']
    fine_msg = int(fine_msg)  # 0은 데이터 못가져온 것, 1은 좋음, 2는 보통, 3은 나쁨, 4는 매우 나쁨
    if fine_msg == 0:
        fine = '데이터를 가져오지 못했습니다.'

    fine = dust_df[dust_df['stationName'] == '성동구'].iloc[0]['pm10Value']
    fine = int(fine)

    global weather, weather_msg
    weather['미세먼지'] = fine
    weather_msg['미세먼지 경보'] = fine_msg  # 0은 데이터 못 가져온 것, 1은 좋음, 2는 보통, 3은 나쁨, 4는 매우 나쁨!!

    print(weather)
    print(weather_msg)

schedule.every().day.at("05:10").do(weather_data)
schedule.every().day.at("05:10").do(fine_dust)


#---------------------------------------------------------------------------------------------

# NUGU RestAPI-----------KIM NAYOUNG------------------------------------------
@csrf_exempt
# answer.weather
# backend parameter: weather_yn, wmessage1, veryhot, verycold, dust, verydry
def odd_weather(request):
    weather_data()
    fine_dust()

    weather_msg = {'폭염': 0, '한파': 1, '건조주의보': 0, '강수메세지': 0, '미세먼지 경보':4}

    weather_alert = []
    ctx = {}
    ctx['wmessage1'] = ""
    lg_app = []

    # check odd weather condition based on data dictionary
    # set parameter value along with the weather condition
    for key, value in weather_msg.items():
        if(value == 1):
            if(key=='폭염'):
                weather_alert.append(key)
                ctx['veryhot'] = 'yes'
                ctx['wmessage1'] += "오늘 폭염주의보가 있어. "
                lg_app.append('에어컨') 
            
            elif(key=='한파'):
                weather_alert.append(key)
                ctx['verycold'] = 'yes'
                ctx['wmessage1'] += "오늘 한파주의보가 있어. "

            elif(key=='건조주의보'):
                weather_alert.append(key)
                ctx['verydry'] = 'yes'
                ctx['wmessage1'] += "오늘 건조주의보가 있어. "
        
        elif(value==3 and key=="미세먼지 경보"):
            weather_alert.append(key)
            ctx['dust'] = 'yes'
            ctx['wmessage1'] += "오늘 미세먼지 지수는 나쁨이야. "
            lg_app.append('공기청정기')      

        elif(value==4 and key=='미세먼지 경보') :
            weather_alert.append(key)
            ctx['dust'] = 'yes'
            ctx['wmessage1'] += "오늘 미세먼지 지수는 매우나쁨이야. "
            lg_app.append('공기청정기')             
    
    if len(lg_app) >= 2:
        ctx['lg'] = " , ".join(lg_app)
    
    if weather_alert:
        ctx["weather_yn"] = str(len(weather_alert))
        # msg = " , ".join(weather_alert)
        # ctx["wmessage1"] = msg

    else:
        ctx["weather_yn"] = "0"
        ctx['wmessage1'] = "오늘 날씨 괜찮네."
    
    # nugu response set
    respon = {
        "version": "2.1",
        "resultCode": "OK",
        "output":ctx,
    }

    return JsonResponse(respon) 

@csrf_exempt
# giving temperature data
def give_temp(request):
    weather_data()
    weather = {'최고기온': 17, '최저기온': 5, '평균습도': 20, '강수확률': 25, '미세먼지': 70}    
    ctx = {}
    high_temp = weather["최고기온"]
    low_temp = weather["최저기온"]

    ctx["tmessage"] = "오늘 최고 기온은 " + str(high_temp) + "도이고, 오늘 최저 기온은 " + str(low_temp) + "도래."
    # nugu response set
    respon = {
        "version": "2.1",
        "resultCode": "OK",
        "output":ctx,
    }

    return JsonResponse(respon) 
    
@csrf_exempt
# giving rain probabilty data
def give_rain_probability(request):
    weather_data()
    # weather = {'최고기온': 17, '최저기온': 5, '평균습도': 20, '강수확률': 25, '미세먼지': 30}
    ctx={}
    rain = weather['강수확률']
    if(rain >= 50) :
        ctx['rmessage'] = "오늘 강수확률 " + str(rain) + "%래. 나갈 때 우산 챙기는 거 잊지마!"
    
    else:
        ctx['rmessage'] = "오늘 강수확률 " + str(rain) + "%래. 확률은 작지만 혹시 모르니까 일기 예보 확인하구."

    # nugu response set
    respon = {
        "version": "2.1",
        "resultCode": "OK",
        "output":ctx,
    }

    return JsonResponse(respon) 

@csrf_exempt
# giving fine-dust number
def give_dust(request):
    weather_data()
    fine_dust()
    # weather = {'최고기온': 17, '최저기온': 5, '평균습도': 20, '강수확률': 25, '미세먼지': 30}
    dust_num = weather['미세먼지']
    ctx={}

    # 보통이 경우
    if(weather_msg['미세먼지 경보'] == 2): 
        ctx['dmessage'] = "오늘의 미세먼지 농도는 " + str(dust_num) + "로 보통이래. 이정도면 나가는 거 괜찮을지도!"
    
    # 아주 좋은 경우
    if(weather_msg['미세먼지 경보'] == 1):
        ctx['dmessage'] = "오늘의 미세먼지 농도는 " + str(dust_num) + "로 좋음이래. 공기가 맑아서 산책이라도 나가면 좋겠다"

    # nugu response set
    respon = {
        "version": "2.1",
        "resultCode": "OK",
        "output":ctx,
    }

    return JsonResponse(respon)