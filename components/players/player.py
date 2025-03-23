from typing import List
from components.llm.llm import LLM
from components.players.prompts import get_discuss_prompt, get_vote_prompt, get_kill_prompt, get_reveal_prompt, get_save_prompt
from components.players.utils import get_role_from_name, sanitize_name, get_human_input

class Player:
    def __init__(self, name: str, is_human: bool = False):
        self.is_human = is_human
        self.name = name
        self.events = []
        if not is_human:
            self.brain = LLM(name)


    def get_type(self):
        return self.__class__.__name__

    def discuss(self, players) -> str:
        if self.is_human:
            return get_human_input("What do you want to say?")
        if not hasattr(self, 'revealed'):
            revealed = ""
        else:
            revealed = self.revealed

        prompt = get_discuss_prompt(
            self.events, 
            self.name, 
            self.get_type(), 
            [p.name for p in players if p.name != self.name],
            revealed
        )
        out = self.brain.chat_completion(prompt)
        return out

    
    def vote(self, players):
        if self.is_human:
            return get_human_input("Who do you want to vote for? Just type the name and nothing else.")
        
        if not hasattr(self, 'revealed'):
            revealed = ""
        else:
            revealed = self.revealed

        prompt = get_vote_prompt(
            self.events, 
            self.name, 
            self.get_type(), 
            [p.name for p in players if p.name != self.name],
            revealed
        )
        out = self.brain.chat_completion(prompt)
        voted =  sanitize_name(out, players)
        return voted

class Werewolf(Player):
    def __init__(self, name: str, is_human: bool = False):
        super().__init__(name, is_human)

    def kill_player(self, players, tries=0) -> str:
        if self.is_human:
            return get_human_input("Who do you want to kill? Just type the name and nothing else.")
        if tries > 3:
            raise ValueError(f"Werewolf {self.name} is too dumb to kill anyone. Game Aborted.")
        prompt = get_kill_prompt(
            self.events, 
            self.name, 
            [p.name for p in players if p.get_type() == 'Werewolf' and p.name != self.name], 
            [p.name for p in players if p.name != self.name]
        )
        out = self.brain.chat_completion(prompt).lower()
        kill_name =  sanitize_name(out, players)

        if kill_name is not None:
            return kill_name
        return self.kill_player(players, tries+1)


class Villager(Player):
    def __init__(self, name: str, is_human: bool = False):
        super().__init__(name, is_human)

class Seer(Player):
    def __init__(self, name: str, is_human: bool = False):
        super().__init__(name, is_human)
        self.revealed = {}

    def reveal(self, players, tries=0) -> str:
        if self.is_human:
            return get_human_input("Who do you want to reveal? Just type the name and nothing else.")
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

        reveal_name = sanitize_name(out, players)

        if self.is_human:
            print(f"Revealing: {reveal_name} is a {get_role_from_name(reveal_name, players)}")
            
        if reveal_name is not None:
            self.revealed[reveal_name] = get_role_from_name(reveal_name, players)
            return reveal_name
        return self.reveal(players, tries+1)

class Doctor(Player):
    def __init__(self, name: str, is_human: bool = False):
        super().__init__(name, is_human)

    def save_player(self, players, tries=0) -> str:
        if self.is_human:
            return get_human_input("Who do you want to save? Just type the name and nothing else.")
        if tries > 3:
            raise ValueError(f"Doctor {self.name} is too dumb to save anyone. Game Aborted.")
        prompt = get_save_prompt(
            self.events, 
            self.name, 
            [p.name for p in players if p.name != self.name]
        )
        out = self.brain.chat_completion(prompt).lower()
        save_name = sanitize_name(out, players)

        if save_name is not None:
            return save_name
        return self.save_player(players, tries+1)

def create_player(name: str, role: str, is_human: bool = False):
    if role == 'Werewolf':
        return Werewolf(name, is_human)
    elif role == 'Villager':
        return Villager(name, is_human)
    elif role == 'Seer':
        return Seer(name, is_human)
    elif role == 'Doctor':
        return Doctor(name, is_human)
    else:
        raise ValueError("WTF was that role?!?!?")