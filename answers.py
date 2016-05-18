import random

def RandomPost(msg, games):
    input = ['во что мне поиграть', 'во что поиграть', 'во что мне проиграть', 'во что проиграть']
    output = ['Попробуй вот это: ', 'Может это? ', 'Ну, попробуй поиграть вот в это: ']
    outputend = [' . Не забудь поставить игре оценку ;)', ' . Репостни, если понравилась!', ' . GLHF!']
    isRight = False
    #print(msg)
    for inp in input:
        if(msg.find(inp) != -1):
            isRight=True
            break
    if(isRight):
        return str(random.choice(output)+ str(getPost(msg, games)) + random.choice(outputend))

def getPost(msg, games):
    phase = msg.split('(')[-1]
    if phase.endswith(')') or phase.endswith(')?') or phase.endswith(') ?'):
        phase = phase[:-1]
        phases = phase.split(',')
        links = list()

        for game in games:
            game.text = game.text.lower()
            #Multiply search
            if(len(phases)>1):
                isRight=False
                for phas in phases:
                    phas.replace(" ", "")
                    if(msg.find(phas) == -1):
                        isRight=False
                        break
                    else:
                        isRight=True
                if(isRight):
                    links.append(game.link)

            #Single search
            if(game.text.find(phase)!= -1):
                links.append(game.link)
        if(len(links)>0):
            return random.choice(links)
        else:
            return random.choice(games).link+' Это рандомная игра, т.к. игр по твоему запросу у нас походу нет :( '
    #Without search
    else:
        return random.choice(games).link

def getHelp(msg):
    input = ["как пользоваться ботом", "что бот умеет"]
    answer = 'Во что поиграть - бот вернет рандомную ссылку с группы \n' \
             'Во что поиграть(Action) - бот ответит рандомной ссылкой на пост, где есть ' \
             'фраза Action(вместо Action можно подставить свою фразу)'
    isRight = False
    #print(msg)
    for inp in input:
        if(msg.find(inp) != -1):
            isRight=True
            break
    if(isRight):
        return answer

