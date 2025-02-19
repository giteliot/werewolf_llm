import random
from typing import List
from components.llm.llm import LLM
from components.players.prompts import get_discuss_prompt, get_vote_prompt

class Player:
    def __init__(self, name: str):
        self.name = name
        self.brain = LLM(name)
        self.events = []

    def get_type(self):
        return self.__class__.__name__

    def discuss(self, players) -> str:
        prompt = get_discuss_prompt(
            self.events, 
            self.name, 
            self.get_type(), 
            [p.name for p in players if p.name != self.name]
        )
        out = self.brain.chat_completion(prompt)
        print(f"""> {self.name}
        {out}
        """)
        return out

    
    def vote(self, players):
        prompt = get_vote_prompt(
            self.events, 
            self.name, 
            self.get_type(), 
            [p.name for p in players if p.name != self.name]
        )
        out = self.brain.chat_completion(prompt)
        print(self.name, out)
        return out

class Werewolf(Player):
    def __init__(self, name: str):
        super().__init__(name)
    def kill_player(self, players) -> str:
        for p in random.sample(players, len(players)):
            if p.get_type() != 'Werewolf':
                return p

class Villager(Player):
    def __init__(self, name: str):
        super().__init__(name)

class Seer(Player):
    def __init__(self, name: str):
        super().__init__(name)

    def reveal(self, players) -> str:
        for p in random.sample(players, len(players)):
            if p.name != self.name:
                self.events.append(f"You (Seer) revealed: {p.name} is a {p.get_type()}")
                return p

class Doctor(Player):
    def __init__(self, name: str):
        super().__init__(name)
    def save_player(self, players) -> str:
        for p in random.sample(players, len(players)):
            if p.get_type() != 'Doctor':
                return p

def create_player(name: str, role: str):
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