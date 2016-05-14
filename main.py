#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vk, time, random, answers#, networkx as nx


def answ(txt):
    while True:
                try:
                    vkapi.messages.send(user_id=message['user_id'],forward_messages=message['id'], message=txt)
                except:

                    continue
                else:

                    break


class Game:
    def __init__(self, link, users, score):
        self.link = link;
        self.users = users;
        self.score = score;
    def __repr__(self):
        return repr((self.link, self.users, self.score))

class User:
    def __init__(self, id, games):
        self.id = id;
        self.games = games;
    def __repr__(self):
        return repr((self.id, self.games))

#Games
games = list()
#Graph of users
#graph = nx.Graph()
#Grop ID
group_id="-53524685";

offset=1

count = 100
session = vk.Session(access_token="TOKEN_HERE!")
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
    #print(feedback)
    for post in feedback['items']:
      if 'attachments' in post:
        for attach in post["attachments"]:
            if attach["type"] == 'poll':
               if len(attach["poll"]["answers"]) == 6:
                        game = Game('https://vk.com/wall'+group_id+'_'+str(post['id']), attach["poll"]["votes"], attach["poll"]["answers"][0]["rate"])
                        games.append(game)
                        #Grapher
               #        while True:
             #               try:
          #                      poll = vkap.polls.getVoters(owner_id=group_id, poll_id = str(attach["poll"]["id"]), answer_ids= str(attach["poll"]["answer_id"]))
           #                     print(poll["users"]["items"])
            #                except:
             #                   numoftry+=1
              #                  print(poll)
               #                 continue
                #            else:
                 #               break
    offset +=count
    #print(str(("Инициализация: ", offset)))

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
         answer = answers.RandomPost(msg, games)
         if answer!=None:
             answ(answer)
         #vkapi.markAsRead(peer_id=message['id'])
    time.sleep(1.5)

