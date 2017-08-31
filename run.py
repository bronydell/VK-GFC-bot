from vk_client import Client
from vk_client import VKPooler
from vk_client import Codes
import saver
import threading
import game_parser
import json
import formatter

def readFile(path):
    try:
        with open(path, encoding='UTF-8') as data_file:
            return data_file.read()
    except Exception as ex:
        print(ex.__str__())

def getSettings():
    try:
        with open('bot.json', encoding='UTF-8') as data_file:
            data = json.load(data_file)
            return data
    except ValueError:
        return None
    except Exception as ex:
        print(ex.__str__())

def performAction(client, update, action):
    if action == 'random':
        answer = formatter.RandomPost(update[6], saver.openPref(client.id, "games", list()))
        client.messages.send(peer_id=update[3], message=answer)

    elif action == 'stats':
        answer = saver.openPref(client.id, "stats", "Ничего не инициализированно")
        client.messages.send(peer_id=update[3], message=answer)
    else:
        settings = getSettings()
        if 'actions' in settings and action in settings['actions']:
            for tag in settings['actions'][action].keys():
                if tag == 'message':
                    client.messages.send(peer_id=update[3], message=settings['actions'][action][tag])

def getForwardedText(message):
    if 'fwd_messages' in message:
        if message['fwd_messages'][0]['body'] == '':
            return getForwardedText(message['fwd_messages'][0])
        else:
            return message['fwd_messages'][0]['body']
    return None

def message(client, update):
    message_text = update[6]
    if 'fwd' in update[7] and message_text == '':
        message = client.messages.getById(message_ids=update[1])['items'][0]
        message_text = getForwardedText(message)
    if message_text is None:
        return
    settings = getSettings()
    for text_message in settings['message']:
        for phase in text_message['keywords']:
            if message_text.lower().startswith(phase.lower()):
                performAction(client, update, text_message['action'])


if saver.openPref("master", "client_key", None) is None:
    client = Client(login=input('Email: '), password=input('Password: '))
    saver.savePref("master", "client_key", client.access_token)
else:
    client = Client(access_token=saver.openPref("master", "client_key", None))

community1 = Client(access_token=readFile('gfc_token.config'),
                    id=-53524685)

community2 = Client(access_token=readFile('gfspc.config'),
                    id=-65820735)

poller = VKPooler()
poller.addHandler(code=Codes.NEW_MESSAGE, function=message)
threading.Timer(0, game_parser.getGames, [client, "-53524685"]).start()
threading.Timer(0, game_parser.getGames, [client, "-65820735"]).start()
poller.startPooling(community1)
poller.startPooling(community2)

