#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vk, time, answers


def answ(txt):
    while True:
                try:
                    vkapi.messages.send(user_id=message['user_id'],forward_messages=message['id'], message=txt)
                except:

                    continue
                else:

                    break



class Game:
    def __init__(self, link, users, score, text):
        self.link = link;
        self.score = score;
        self.text = text;
    def __repr__(self):
        return repr((self.link, self.users, self.score, self.text))

#Games
games = list()
#Graph of users
#graph = nx.Graph()
#Grop ID
group_id="-53524685";

offset=1

count = 100
session = vk.Session(access_token="5596e7e43c5b0638834d2a147ca4439c4c216c702298aff10a9c12528ea154aadd803139fa0ec50354bd6")
session2= vk.Session()
vkapi = vk.API(session, timeout=10, v='5.50')
vkap = vk.API(session2, timeout=10, v='5.50')

numoftry=0
while offset+count <= 3224:



    while True:
        try:
            feedback = vkap.wall.get(owner_id=group_id, offset = str(offset), count=str(count), filter="owner", extended="0")
        except:
            numoftry+=1
            print("DAFUQ?")
            continue
        else:

            break
    for post in feedback['items']:
      if 'attachments' in post:
        for attach in post["attachments"]:
            if attach["type"] == 'poll':
               if len(attach["poll"]["answers"]) == 6:
                        game = Game('https://vk.com/wall'+group_id+'_'+str(post['id']), attach["poll"]["votes"], attach["poll"]["answers"][0]["rate"], post['text'])
                        games.append(game)
    offset +=count
    print(str(("Initilization progress: ", offset)))
print('Inited!')
numoftry=0
while True:
    while True:
        try:
           dic = vkapi.messages.get(count=100, out=0, filters=0)
        except:
            numoftry+=1

            continue
        else:

            break

    for message in dic["items"]:
        msg = message['body'].lower()
        if message['read_state'] == 0:
         #print(message['body'])
         answer = answers.getHelp(msg)
         if answer!=None:
             answ(answer)
         answer=None
         answer = answers.RandomPost(msg, games)
         if answer!=None:
             answ(answer)
         #vkapi.markAsRead(peer_id=message['id'])
    time.sleep(1.5)

