from components.game import Game

if __name__ == "__main__":
    game = Game([
        'Werewolf','Werewolf',
        'Villager','Villager','Villager',
        'Seer','Doctor'])

    
    for _ in range(1000):
        out = game.play_step()
        if out < 0:
            break

