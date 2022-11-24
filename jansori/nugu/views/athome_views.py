from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from datetime import datetime, time, timedelta

ex_date = datetime(2022, 11, 20) # date and time format
eat_time = datetime(2022, 11, 24, 12, 0) # date and time format
clean_date = datetime(2022, 11, 15)
clean_cycle = 7

def what_user_did():
    did_what = {}
    if (datetime.now() - ex_date).days:
        did_what['ex_did'] = "no"
    else:
        did_what['ex_did'] = "yes"
    
    if datetime.today().day != eat_time.day:
        did_what['eat_did'] = "no"
    else:
        did_what['eat_did'] = "yes"

    if (datetime.now() - clean_date).days:
        did_what['clean_did'] = "no"
    else:
        did_what['clean_did'] = "yes"        
    
    return did_what

def msg_for_ex():
    ex_no_day = int((datetime.now() - ex_date).days)
    # if user didn't do the excercise 1, 2 days
    if ex_no_day == 1:
        hmessage = "와 어제 운동 했네! 아직 운동할 시간 있어! 화이팅 해보자구."
        
    elif ex_no_day == 2:
        hmessage = "운동을 하지 않은지 이틀차야! 오늘 운동 계획 있다고 믿어."
        
    # if user didn't do the excercise more than 3 days(ex_no_day = 1, 2)
    else:
        hmessage = "운동 안 한지 벌써 " + str(ex_no_day) + "일째야. 운동 추천 영상 tv에 틀었어. 다른 영상을 보고 싶으면 앱에서 선택할 수 있어. 우리 매일 스트레칭 1분이라도 하자! 앱에 기록하는 거 잊지말구."
        
    return hmessage

def msg_for_clean():
    clean_not_day = int((datetime.now() - clean_date).days)

    if clean_not_day > clean_cycle:
        hmessage = "설정해둔 청소주기가 지났어. 청소를 안 한지 벌써" + str(clean_not_day) + "일이 되었어. 청소기라도 살짝 밀어볼까?"

    else:
        hmessage = "아직 설정한 청소주기가 돌아오지 않았어. 그래도 눈에 보이는 쓰레기가 있다면 치우는 거 잊지 말기!"

    return hmessage

@csrf_exempt
# answer.athome
def answer_athome(request):    
    ctx = {}
    ctx['hmessage'] = ""
    user_did = what_user_did()
    print(user_did)
    eat_num = 2 # integer number    
    ctx["ex_not_day"] = str((datetime.now() - ex_date).days)
    print(ctx)
    count = 0
    not_did_list = []
    for key, value in user_did.items():
        if value == "no":
            count += 1
            not_did_list.append(key)

    # 1. when user did everything
    if count == 0:
        ctx['hmessage'] = "오늘 운동도 하고, 밥도 먹고, 청소도 했어? 완전 갓생살았네!"

    # 2. when user didn't do one thing
    elif count == 1: 
        if "ex_did" in not_did_list:
            if eat_num == 1:
                ctx['hmessage'] += "오늘 왜 한끼만 먹었어어. 잘 챙겨먹는 것도 엄청 중요해! "

            ctx['hmessage'] += msg_for_ex()

        elif "eat_did" in not_did_list:
            ctx['hmessage'] += "헉 오늘 한끼도 안먹었어? 기록을 안한 거라면 앱에서 기록해줘. 아니면 밥 잘 챙겨먹고 다녀어. 한국인은 밥심!"
        
        else:
            if eat_num == 1:
                ctx['hmessage'] += "오늘 왜 한끼만 먹었어어. 잘 챙겨먹는 것도 엄청 중요해! "
            
            ctx['hmessage'] += msg_for_clean()
    
    # 3. when user didnt' do over 2 things
    else:
        first_msg = "으으음 많이 놀았으니까 자신을 위해서 일을 해볼까? "
        ctx['hmessage'] = first_msg

        if "ex_did" in not_did_list:
            if eat_num == 1:
                ctx['hmessage'] += "오늘 왜 한끼만 먹었어어. 잘 챙겨먹는 것도 엄청 중요해! "

            ex_msg = msg_for_ex()
            ctx['hmessage'] = ctx['hmessage'] + ex_msg + " "

        if "eat_did" in not_did_list:
            eat_msg = "헉 오늘 한끼도 안먹었어? 기록을 안한 거라면 앱에서 기록해줘. 아니면 밥 잘 챙겨먹고 다녀어. 한국인은 밥심!"
            ctx['hmessage'] = ctx['hmessage'] + eat_msg + " "

        if "clean_did" in not_did_list:
            if eat_num == 1:
                ctx['hmessage'] += "오늘 왜 한끼만 먹었어어. 잘 챙겨먹는 것도 엄청 중요해! "

            clean_msg = msg_for_clean()
            ctx['hmessage'] = ctx['hmessage'] + clean_msg + " "
    
    respon = {
        "version": "2.0",
        "resultCode": "OK",
        "output":ctx,
    }

    return JsonResponse(respon)     