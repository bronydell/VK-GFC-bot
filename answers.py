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
        return str(random.choice(output)+ random.choice(games).link + random.choice(outputend))


