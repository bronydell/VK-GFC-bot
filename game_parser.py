import saver
import threading

# Объект игры
class Game:
    def __init__(self, link, users, score, text):
        self.link = link
        self.score = score
        self.text = text

    def __repr__(self):
        return repr((self.link, self.users, self.score, self.text))


def getGames(client, group_id):
    games = list()
    offset = 1
    count = 100

    feedback = client.wall.get(owner_id=group_id, offset=offset, count=count, filter="owner", extended=0)
    available = feedback['count']
    # Алгоритм сбора информации
    # 1. Берем все посты и фасуем в обхекты
    # 2. Не фасуем в объект, если нет 6 вариантов опроса(5, 4, 3, 2, 1, Результат)
    # 3. Обнволяем массив
    while offset <= available:

        feedback = client.wall.get(owner_id=group_id, offset=offset, count=count, filter="owner", extended=0)

        # print('YO!')
        for post in feedback['items']:
            if 'attachments' in post:
                for attach in post["attachments"]:
                    if attach["type"] == 'poll':
                        if len(attach["poll"]["answers"]) == 6:
                            game = Game('https://vk.com/wall' + group_id + '_' + str(post['id']),
                                        attach["poll"]["votes"], attach["poll"]["answers"][0]["rate"], post['text'])
                            games.append(game)
        offset += count
    # Функция f() вызывается 1 раз в день
    from datetime import datetime
    saver.savePref(group_id, "games", games)
    saver.savePref(group_id, "stats", '(' + str(datetime.now()) + ') Inited ' + str(len(games)) + ' posts!')
    threading.Timer(60 * 60 * 24, getGames, [client, group_id]).start()
