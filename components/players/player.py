import random
from typing import List

class Player:
    def __init__(self, name: str):
        self.name = name
        self.events = []
        self.conversations = []

    def get_type(self):
        return self.__class__.__name__
    
    def vote(self, players: List[Player]) -> Player:
        for p in random.sample(players, len(players)):
            if p.name() != self.name:
                return p

class Werewolf(Player):
    def __init__(self, name: str):
        super().__init__(name)
    def kill_player(self, players: List[Player]) -> str:
        for p in random.sample(players, len(players)):
            if p.get_type() != 'Werewolf':
                return p

class Villager(Player):
    def __init__(self, name: str):
        super().__init__(name)

class Seer(Player):
    def __init__(self, name: str):
        super().__init__(name)

    def reveal(self, players: List[Player]) -> str:
        revealed = players[0]
        self.events.append(f"You (Seer) revealed: {revealed.name} is a {revealed.get_type()}")
        return revealed

class Doctor(Player):
    def __init__(self, name: str):
        super().__init__(name)
    def save_player(self, players: List[Player]) -> str:
        for p in random.sample(players, len(players)):
            if p.get_type() != 'Doctor':
                return p

def create_player(name: str, role: str) -> Player:
    if role == 'Werewolf':
        return Werewolf(name)
    elif role == 'Villager':
        return Villager(name)
    elif role == 'Seer':
        return Seer(name)
    elif role == 'Doctor':
        return Doctor(name)
    else:
        raise ValueError("WTF was that role?!?!?")