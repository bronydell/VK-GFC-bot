import random
import recomender

group_id = "-53524685"

#Берем рандомный пост, если есть одна из фраз, что в input[]
def RandomPost(msg, games):
    output = ['Попробуй вот это: ', 'Может это? ', 'Ну, попробуй поиграть вот в это: ']
    outputend = [' . Не забудь поставить игре оценку ;)', ' . Репостни, если понравилась!', ' . GLHF!']
    return str(random.choice(output)+ str(getPost(msg, games)) + random.choice(outputend))

'''def getRecommendations(message, dataset):
    input = ['порекомендуй игру', 'порекомендуй игры']
    isRight = False
    #print(msg)
    msg = message['body'].lower()
    for inp in input:
        #Ищем что-то
        if(msg.find(inp) != -1):
            isRight=True
            break
    #Нашли! Отвечаем
    if(isRight):
        try:
            result = recomender.getRecommendations(dataset, str(message["user_id"]))
            i = 0
            #print(result)
            answer = "Вот результаты за сегодня, составленые специально для тебя: \n"
            while(i<10):
                answer+=str(i+1)+". https://vk.com/wall"+group_id+"_"+str(result[i][1])+"\n"
                i+=1
            return answer
        except:
            return 'Вы не учавствали в опросах группы. Зайдите в группу и проголосуйте за игры, в которые вы играли'
'''

#Подбиваем пост под поиск
def getPost(msg, games):
    #Делим сообщение на скобки и берем все что внутри последней
    phase = msg.split('(')[-1]
    if phase.endswith(')') or phase.endswith(')?') or phase.endswith(') ?'):
        phase = phase[:-1]


        #Массив запросов на поиск в сообещниий(Например, (Warcraft, RPG))
        phases = phase.split(',')
        links = list()
        for game in games:
            game.text = game.text.lower()
            #Если мультипоиск(больше одного запроса)
            isRight=False
            for phras in phases:

                phras.strip()
                if game.text.find(" "+phras.lower()+" ") == -1:
                    isRight = False
                    break
                else:
                    isRight=True
            if(isRight):
                links.append(game.link)
        #Нашли что-то. Пикаем
        if(len(links)>0):
            return random.choice(links)
        else:
        #Не нашли. Даем рандомную игру
            return random.choice(games).link+' Это рандомная игра, т.к. игр по твоему запросу у нас походу нет :( '
    #Без поиска
    else:
        return random.choice(games).link
#FAQ по ключевым словам
def getHelp(msg):
    input = ["как пользоваться ботом", "что бот умеет"]
    answer = 'Во что поиграть - бот вернет рандомную ссылку с группы \n' \
             'Во что поиграть(Action) - бот ответит рандомной ссылкой на пост, где есть ' \
             'фраза Action(вместо Action можно подставить свою фразу)'
    isRight = False
    #print(msg)
    for inp in input:
        if(msg.find(inp.lower()) != -1):
            isRight=True
            break
    if(isRight):
        return answer

def getStat(msg, stat):
    input = ["статистика"]
    isRight = False
    for inp in input:
        if(msg.find(inp) != -1):
            isRight=True
            break
    if(isRight):
        return stat