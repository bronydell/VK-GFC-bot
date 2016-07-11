#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vk, time, answers
import threading
import recomender
import botan


with open('botan.config', 'r') as myfile:  # Засунь ключ от botana в botan.config!!! ЭТО ВАЖНО!!!!
    botan_token = myfile.read().replace('\n', '')


# Объект игры
class Game:
    def __init__(self, link, users, score, text):
        self.link = link;
        self.score = score;
        self.text = text;

    def __repr__(self):
        return repr((self.link, self.users, self.score, self.text))


# ID группы
group_id = "-53524685"
# Глобальная переменная массива игр
games = list()
# Dataset
dataset = None
# Бета тестеры
testers = list()
# Статистика
stats = "???"
# count для опросов
pollcount = 1000

def deleteContent(fName):
    with open(fName, "w"):
        pass


def getGames(vkap):
    global games
    global dataset
    dataset = None
    games = list()
    # deleteContent("db.dat")
    offset = 1
    count = 100
    while True:
        try:
            feedback = vkap.wall.get(owner_id=group_id, offset=str(offset), count=str(count), filter="owner",
                                     extended="0")
        except:
            continue
        else:
            break
    available = feedback['count']
    # Алгоритм сбора информации
    # 1. Берем все посты и фасуем в обхекты
    # 2. Не фасуем в объект, если нет 6 вариантов опроса(5, 4, 3, 2, 1, Результат)
    # 3. Обнволяем массив
    while offset + count <= available:
        while True:
            try:
                feedback = vkap.wall.get(owner_id=group_id, offset=str(offset), count=str(count), filter="owner",
                                         extended="0")
            except:
                continue
            else:
                break
        # print('YO!')
        for post in feedback['items']:
            print(str(post['id']))
            if 'attachments' in post:
                for attach in post["attachments"]:
                    if attach["type"] == 'poll':
                        if len(attach["poll"]["answers"]) == 6:
                            game = Game('https://vk.com/wall' + group_id + '_' + str(post['id']),
                                        attach["poll"]["votes"], attach["poll"]["answers"][0]["rate"], post['text'])
                            games.append(game)
                        print(str(post['id']))
                        # Получаем все результаты опросов и ВСЕ записываем в db.dat
                        ids = ""
                        for answer in attach["poll"]["answers"]:
                            ids += str(answer["id"]) + ", "
                        ids = ids[:-2]
                        poll_offset = 0
                        while True:
                            try:
                                resp = vkap.polls.getVoters(owner_id=group_id, answer_ids=ids,
                                                            poll_id=attach["poll"]['id'],
                                                            offset=poll_offset, count=pollcount)
                            except vk.exceptions.VkAPIError as d:

                                # print(d)
                                if (d.code == 6):
                                    time.sleep(1)
                                else:
                                    poll_offset += pollcount
                                    break
                                continue

                            except Exception:
                                print('Miracle!')
                                continue
                            else:

                                poll_offset += pollcount
                                break

                        i = 0
                        counters = [0] * 6
                        for answ in resp:
                            counters[i] = answ["users"]["count"]
                        while poll_offset - pollcount <= max(counters):
                            i = 5
                            for answ in resp:

                                for voter in answ["users"]["items"]:
                                    with open("db.dat", "a") as myfile:
                                        if (i != 0):
                                            myfile.write(str(voter) + " " + str(post['id']) + " " + str(i) + "\n")

                                i -= 1
                            while True:
                                try:
                                    resp = vkap.polls.getVoters(owner_id=group_id, answer_ids=ids,
                                                                poll_id=attach["poll"]['id'],
                                                                offset=poll_offset, count=pollcount)
                                except vk.exceptions.VkAPIError as d:

                                    # print(d)
                                    if (d.code == 6):
                                        time.sleep(1)
                                    else:
                                        poll_offset += pollcount
                                        break
                                    continue
                                except Exception:
                                    time.sleep(0.5)
                                    continue
                                else:

                                    poll_offset += pollcount
                                    break
        offset += count
    dataset = recomender.loadDataset("db.dat")
    # Функция f() вызывается 1 раз в день
    from datetime import datetime
    stats = '(', str(datetime.now()), ') Inited ', len(games), ' posts!';
    threading.Timer(60 * 60 * 24, getGames, [vkap]).start()


def initBeters(vkap):
    while True:
        try:
            resp = vkap.groups.getMembers(group_id=123439288, count=1000)
        except vk.exceptions.VkAPIError as d:

            # print(d)
            if (d.code == 6):
                time.sleep(1)
            else:
                break
            continue

        except Exception:
            print('Miracle!')
            continue
        else:
            break

    global testers
    testers = resp['items']
    threading.Timer(60 * 60, initBeters, [vkap]).start()




def isBetaTester(message):
    if message['user_id'] in testers == True:
        return True
    else:
        return False

# Проверка обновлений
def refreshMessages(vkapi):
    # print(len(games))
    if (len(games) > 0 and dataset is not None):
        # print('HERE WE GO!')
        while True:
            try:
                dic = vkapi.messages.get(count=100, out=0, filters=0)
                # print(dic)
            except:
                continue
            else:
                break

        for message in dic["items"]:
            msg = message['body'].lower()
            # print(msg)
            if message['read_state'] == 0:
                answer = answers.getRecommendations(message, dataset)
                print(answer)
                if answer != None and isBetaTester(message):
                    answ(message, answer, 'Recommendation!')
                    answer = None
                elif answer != None:
                    answ(message, "Ты не бета тестер!", "Non Beta")
                    answer=None
                answer = answers.getStat(message, stats)
                if answer != None:
                    answ(message, answer, 'Help')
                    answer = None
                answer = answers.getHelp(message)
                if answer != None:
                    answ(message, answer, 'Help')
                    answer = None
                answer = answers.RandomPost(msg, games)
                if answer != None:
                    answ(message, answer, 'Random post')
                    # print(answer)
    threading.Timer(1, refreshMessages, [vkapi]).start()


# Шаблонный ответ
def answ(message, txt, event):
    uid = message['user_id']
    message_dict = txt
    event_name = event
    botan.track(botan_token, uid, message_dict, event_name)
    while True:
        try:
            vkapi.messages.send(user_id=message['user_id'], forward_messages=message['id'], message=txt)
        except:

            continue
        else:

            break


with open('key.config', 'r') as myfile:  # Засунь ключ сообщества в key.config!!! ЭТО ВАЖНО!!!!
    key = myfile.read().replace('\n', '')

with open('userkey.config', 'r') as myfile:  # Засунь ключ сообщества в userkey.config!!! ЭТО ВАЖНО!!!!
    userkey = myfile.read().replace('\n', '')

session = vk.Session(access_token=key)  # Создание сессии
session2 = vk.Session(access_token=userkey)
vkapi = vk.API(session, timeout=10, v='5.50')
vkap = vk.API(session2, timeout=10, v='5.50')

# Поток обработки игр...
getGames(vkap)
# Поток ответов...
refreshMessages(vkapi)
# Поток тестеров...
initBeters(vkap)
