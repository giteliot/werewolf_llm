import random
from typing import List
from components.llm.llm import LLM
from components.players.prompts import get_discuss_prompt, get_vote_prompt, get_kill_prompt, get_reveal_prompt, get_save_prompt
from components.players.utils import get_role_from_name

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

    def kill_player(self, players, tries=0) -> str:
        if tries > 3:
            raise ValueError(f"Werewolf {self.name} is too dumb to kill anyone. Game Aborted.")
        prompt = get_kill_prompt(
            self.events, 
            self.name, 
            [p.name for p in players if p.get_type() == 'Werewolf' and p.name != self.name], 
            [p.name for p in players if p.name != self.name]
        )
        out = self.brain.chat_completion(prompt).lower()
        kill_name = None
        for p in players:
            if p.name in out:
                kill_name = p.name
                break

        if kill_name is not None:
            return kill_name
        return self.kill_player(players, tries+1)


class Villager(Player):
    def __init__(self, name: str):
        super().__init__(name)

class Seer(Player):
    def __init__(self, name: str):
        super().__init__(name)
        self.revealed = {}

    def reveal(self, players, tries=0) -> str:
        if tries > 3:
            raise ValueError(f"Seer {self.name} is too dumb to reveal anyone. Game Aborted.")

        alive_revealed = {}
        for p in players:
            if p.name == self.name:
                continue
            alive_revealed[p.name] = "unknown"
            if p.name in self.revealed:
                alive_revealed[p.name] = self.revealed[p.name]

        prompt = get_reveal_prompt(
            self.events, 
            self.name, 
            alive_revealed
        )

        out = self.brain.chat_completion(prompt).lower()
        reveal_name = None
        for p in players:
            if p.name in out:
                reveal_name = p.name
                break

        if reveal_name is not None:
            self.revealed[reveal_name] = get_role_from_name(reveal_name, players)
            return reveal_name
        return self.reveal(players, tries+1)

class Doctor(Player):
    def __init__(self, name: str):
        super().__init__(name)

    def save_player(self, players, tries=0) -> str:
        if tries > 3:
            raise ValueError(f"Doctor {self.name} is too dumb to save anyone. Game Aborted.")
        prompt = get_save_prompt(
            self.events, 
            self.name, 
            [p.name for p in players if p.name != self.name]
        )
        out = self.brain.chat_completion(prompt).lower()
        save_name = None
        for p in players:
            if p.name in out:
                save_name = p.name
                break

        if save_name is not None:
            return save_name
        return self.save_player(players, tries+1)

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