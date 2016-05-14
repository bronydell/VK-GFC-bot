import random

def RandomPost(msg, games):
    input = ['во что мне поиграть','во что поиграть', 'во что мне проиграть', 'во что проиграть']
    output = ['Попробуй вот это: ','Может это? ', 'Ну, попробуй поиграть вот в это: ']
    outputend = [' . Не забудь поставить игре оценку ;)',' . Репостни, если понравилась!', ' . GLHF!']
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
    #print(phase)
    if phase.endswith(')'):
        phase = phase[:-1]
        links = list()
        for game in games:
            if(game.text.find(phase)!= -1):
                links.append(game.link)
        if(len(links)>0):
            return random.choice(links)
        else:
            return random.choice(games).link+' Это радомная игра, т.к. игр по твоему запросу у нас походу нет :( '
    else:
        return random.choice(games).link

