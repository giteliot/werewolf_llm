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
    
    for _ in range(100):
        out = game.play_step()
        if out < 0:
            with open('./results/game_result.txt', 'w') as f:
                winner = "Werewolves" if out == -12 else "Villagers"
                f.write(f"Game won by: {winner}\n")
                for name, role in zip(names, roles):
                    f.write(f"{name}: {role}\n")

            print(f"the roles were: {list(zip(names, roles))}")
            break
