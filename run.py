import random
from datetime import datetime
from components.game import Game
from components.llm.llm import MODELS

if __name__ == "__main__":
    names = random.sample(list(MODELS.keys()), len(MODELS.keys()))
    roles = [
        'Werewolf',
        'Villager','Villager',
        'Seer','Doctor']

    logs = []
    game = Game(list(zip(names, roles)), logs)
    
    for _ in range(100):
        out = game.play_step()
        if out < 0:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M")
            with open(f'./results/{timestamp}.txt', 'w') as f:
                winner = "Werewolves" if out == -12 else "Townsfolk"
                logs.append(f"Game won by: {winner}")
                for name, role in zip(names, roles):
                    logs.append(f"{name}: {role}")
                f.write("\n".join(logs))

            # print(f"the roles were: {list(zip(names, roles))}")
            break
