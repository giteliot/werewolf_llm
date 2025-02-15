from components.game import Game

if __name__ == "__main__":
    game = Game([
        'Werewolf','Werewolf',
        'Villager','Villager','Villager',
        'Seer','Doctor'])

    for i in range(len(game.state_handlers)):
        game.play_step()
