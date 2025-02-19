import random
from components.game import Game
from components.llm.llm import MODELS

if __name__ == "__main__":
    names = random.sample(list(MODELS.keys()), 7)
    roles = [
        'Werewolf','Werewolf',
        'Villager','Villager','Villager',
        'Seer','Doctor']

    game = Game(list(zip(names, roles)))

    # TODO create team werewolf and team village
    # based on output, store who won and who lost
    
    for _ in range(6):
        out = game.play_step()
        if out < 0:
            break
