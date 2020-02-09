from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import vk
import random
import database

session = vk.Session(access_token='99f1d574d60a4cbc5df0fb5f3edb1d2cd735fc46299a3f8ff4953791e7f7d78ee105dc26d36b5c0f0428a')
vk_api = vk.API(session)

def talk(request):
    body = json.loads(request.body)
    data = database.get_db()
    user_id =body["object"]["message"]["from_id"]
    stopne = 0
    # print(body)
    # if body == { "type": "confirmation", "group_id": 175960072 }:
    #     return HttpResponse("34c03ca2")
    # print(body)
    # if body["type"] == 'message_new':
    #     data = database.get_db()
    #     user_id = body["object"]["message"]["from_id"]
    #     stocne = 0
    if body["object"]["message"]["text"].find('/') != -1:
        nes = body["object"]["message"]["text"].split('/')
        database.insert_db(nes[0],nes[1])
        vk_api.messages.send(user_id=user_id, message="Я записал новое сообщение", random_id=random.randint(1,50000000000000000000000000) , v=5.103)
    else:
        for i in data:
            if i[1] == body["object"]["message"]["text"]:
                messages = i[2]
                vk_api.messages.send(user_id=user_id, message=messages, random_id=random.randint(1,50000000000000000000000000) , v=5.103)
                stopne = 1
            elif i == data[-1] and i[1] != body["object"]["message"]["text"] and stopne != 1:
                message1 = "Простите, но я не могу ответить так как этого нет в моей базе данных."
                message2 = "Чтобы добавить что-то новое базу данных сообщений напиши Сообщение-Ответ и поставь /."
                vk_api.messages.send(user_id=user_id, message=message1, random_id=random.randint(1,50000000000000000000000000) , v=5.103)
                vk_api.messages.send(user_id=user_id, message=message2, random_id=random.randint(1,50000000000000000000000000) , v=5.103)

@csrf_exempt
def admin(request):
    with open('Weapon/templates/index.html', 'r') as file:
        return HttpResponse(file.read())

@csrf_exempt
def script(request):
    with open('Weapon/templates/script.js', 'r') as file:
        return HttpResponse(file.read())

@csrf_exempt
def client_server(request):
    body = json.loads(request.body)
    res = {}
    if body["type"] == "login":
        if (body["username"] == "admin") and (body["password"] == "admin"):
            res["correct"] = True
            res["val"] = database.get_groups()
            with open('Weapon/templates/Admin.html', 'r') as file:
                res["html"] = file.read()
        else:
            res["correct"] = False
            print(res)
        return HttpResponse(json.dumps(res))
    elif body["type"] == "postNewMessage":
        users_chat_id = database.get_member(body["group"])
        # print("Check dV")
        for i in users_chat_id:
            vk_api.messages.send(user_id=i, message=body['content'], random_id=random.randint(1,50000000000000000000000000) , v=5.103)
        return HttpResponse(json.dumps({"res":"ok"}))

@csrf_exempt
def get_message(request):
    body = json.loads(request.body)
    if body == { "type": "confirmation", "group_id": 175960072 }:
        return HttpResponse("34c03ca2")
        
    print(body)
    if body["type"] == 'message_new':
        if "payload" in body["object"]["message"]:
            if body["object"]["message"]["payload"] == '{"command":"start"}':
                start(request)
            else:
                user_id = body["object"]["message"]["from_id"]
                group = body["object"]["message"]["payload"]
                database.add_member(group,user_id)
        else:
            talk(request)
    return HttpResponse("ok")

def start(request):
    body = json.loads(request.body)
    user_id = body["object"]["message"]['from_id']
    message = "Здравствуйте чтобы получать уведомления о поступления, оружия которое вам интересно, нажмите на одну из кнопок."
    Keyboard = {
        "one_time": True,
        "buttons": [
            [
                {
                    "action": {
                        "type": "text",
                        "payload": '{"command":"gunshot"}',
                        "label": "Огнестрел."
                    },
                    "color": "primary"
                },
                {
                    "action": {
                        "type": "text",
                        "payload": '{"command":"cold"}',
                        "label": "Холодное."
                    },
                    "color": "primary"
                },
                {
                    "action": {
                        "type": "text",
                        "payload": '{"command":"all"}',
                        "label": "Всё оружие."
                    },
                    "color": "primary"
                },
            ]
        ]
    }
    vk_api.messages.send(user_id=user_id, message=message, keyboard=json.dumps(Keyboard), random_id=random.randint(1,50000000000000000000000000) , v=5.103)