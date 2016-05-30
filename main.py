#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vk, time, answers
import threading
import os
import botan, logging


with open('botan.config', 'r') as myfile: #You must put key for your bot in botan.config!!! IMPORTANT!!!!
    botan_token=myfile.read().replace('\n', '')

class Game:
    def __init__(self, link, users, score, text):
        self.link = link;
        self.score = score;
        self.text = text;
    def __repr__(self):
        return repr((self.link, self.users, self.score, self.text))

#Grop ID
group_id="-53524685";
#Global varible games
games = list()



def getGames(vkap):
    global games
    games = list()
    offset = 1
    count = 100
    while True:
            try:
                feedback = vkap.wall.get(owner_id=group_id, offset = str(offset), count=str(count), filter="owner", extended="0")
            except:
                print("DAFUQ?")
                continue
            else:
                break
    available=feedback['count']
    #Alhorithm
    while offset+count <= available:
        while True:
            try:
                feedback = vkap.wall.get(owner_id=group_id, offset = str(offset), count=str(count), filter="owner", extended="0")
            except:
                print("DAFUQ?")
                continue
            else:
                break
        #print('YO!')
        for post in feedback['items']:
            if 'attachments' in post:
                for attach in post["attachments"]:
                    if attach["type"] == 'poll':
                        if len(attach["poll"]["answers"]) == 6:
                            game = Game('https://vk.com/wall'+group_id+'_'+str(post['id']), attach["poll"]["votes"], attach["poll"]["answers"][0]["rate"], post['text'])
                            games.append(game)
        offset +=count
    # call f() again in one day
    from datetime import datetime
    print('(', str(datetime.now()),') Inited ', len(games), ' posts!')
    threading.Timer(60*60*24, getGames, [vkap]).start()


def refreshMessages(vkapi):
    #print(len(games))
    if(len(games)>0):
        #print('HERE WE GO!')
        while True:
            try:
                dic = vkapi.messages.get(count=100, out=0, filters=0)
                #print(dic)
            except:
                continue
            else:
                break

        for message in dic["items"]:
            msg = message['body'].lower()
            #print(msg)
            if message['read_state'] == 0:
                answer = answers.getHelp(msg)
                if answer!=None:
                    answ(message, answer, 'Help')
                    answer=None
                answer = answers.RandomPost(msg, games)
                if answer!=None:
                    answ(message, answer, 'Random post')
                #print(answer)
    threading.Timer(1, refreshMessages, [vkapi]).start()

def answ(message, txt, event):
    uid = message['user_id']
    message_dict = txt
    event_name = event
    botan.track(botan_token, uid, message_dict, event_name)
    while True:
                try:
                    vkapi.messages.send(user_id=message['user_id'],forward_messages=message['id'], message=txt)
                except:

                    continue
                else:

                    break



with open('key.config', 'r') as myfile: #You must put key for your bot in botan.config!!! IMPORTANT!!!!
    key=myfile.read().replace('\n', '')
session = vk.Session(access_token=key)
session2= vk.Session()
vkapi = vk.API(session, timeout=10, v='5.50')
vkap = vk.API(session2, timeout=10, v='5.50')

#Thread Games of...
getGames(vkap)
#Thread Answers of...
refreshMessages(vkapi)



