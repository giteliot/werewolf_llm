import random
from datetime import datetime
from components.game import Game
from components.llm.llm import MODELS

def run(game, names, roles):
    start_time = datetime.now()
    for k in range(40):
        print(f"Step: {k+1}")
        out = game.play_step()
        if out < 0:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            with open(f'./results/{timestamp}.txt', 'w') as f:
                winner = "Werewolves" if out == -12 else "Townsfolk"
                game.logs.append(f"Game won by: {winner}")
                for name, role in zip(names, roles):
                    game.logs.append(f"{name}: {role}")
                f.write("\n".join(game.logs))

            break
    
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"Game duration: {duration}")

def single_run():
    names = random.sample(list(MODELS.keys()), len(MODELS.keys()))
    roles = [
        'Werewolf',
        'Villager','Villager',
        'Seer','Doctor']

    game = Game(list(zip(names, roles)))
    run(game, names, roles)

def all_roles_run():
    names = random.sample(list(MODELS.keys()), len(MODELS.keys()))
    roles = [
        'Werewolf',
        'Villager','Villager',
        'Seer','Doctor']
    
    for _ in range(len(MODELS.keys())):
        game = Game(list(zip(names, roles)))
        run(game, names, roles)
        names = names[-1:] + names[:-1]
    
    game = Game(list(zip(names, roles)))
    run(game, names, roles)

if __name__ == "__main__":
    all_roles_run()


    

