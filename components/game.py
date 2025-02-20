from typing import List, Tuple
from .players.player import create_player, Player
import random
from collections import Counter
from components.players.utils import get_role_from_name

class Game:
    def __init__(self, players: List[Tuple[str, str]]):
        self.players: List[Player] = [create_player(name, role) for name, role in players]
        self.state = 0
        self.night_dead = None

        self.state_handlers = {
            0: self._n0,
            1: self._n1,
            2: self._n2,
            3: self._d0,
            4: self._d1,
            5: self._d2
        }

        self._setup()

    def _setup(self):
        print("Telling players who they are")
        for player in self.players:
            player.events.append(f"A new game begins, {player.name}!")
            player.events.append(f"Your role is {player.get_type()}.")
        print("Revealing Werewolves")
        for p1 in self.get_players('Werewolf'):
            for p2 in self.get_players('Werewolf'):
                if p1 != p2:
                    p1.events.append(f"{p2.name} is another Werewolf! You are allied in this game.")

    def get_players(self, role: str) -> List[Player]:
        return [player for player in self.players if player.__class__.__name__ == role]

    def remove_player(self, player_name: str):
        self.players = [player for player in self.players if player.name != player_name]

    def reveal_event_to_players(self, event_description):
        print()
        print(event_description)
        for p in self.players:
            p.events.append(event_description)

    def reveal_conversation_to_players(self, player, message):
        print()
        # print(f"{player.name} said: {message}")
        for p in self.players:
            if p.name != player.name:
                p.events.append(f"{player.name} said: {message}")
            else:
                p.events.append(f"You said: {message}")

    def play_step(self) -> int:
        self.state_handlers[self.state]()
        self.state += 1
        if self.state > len(self.state_handlers) - 1:
            self.state = 0
        return self.state

    def check_win_condition(self) -> int:
        werewolves = self.get_players('Werewolf')
        if len(werewolves) == 0:
            print("Villagers win!")
            return 1

        village = len(self.players)-len(werewolves)
        if village == 0:
            print("Werewolves win!")
            return -1
        
        return 0

    def _n0(self):
        self.reveal_event_to_players("The night falls. Everyone goes to sleep. Werewolves wake up. Who do you want to kill?")
        werewolf = random.sample(self.get_players('Werewolf'), 1)[0]
        dead = werewolf.kill_player(self.players)
        self.night_dead = dead

    def _n1(self):
        self.reveal_event_to_players("The werewolves made their choise. Seer, wake up. Who do you want to reveal?")
        seer = self.get_players('Seer')
        if len(seer) < 1:
            return
        seer = seer[0]
        seer.reveal(self.players)

    def _n2(self):
        self.reveal_event_to_players("The Seer made their choise. Doctor, wake up. Who do you want to save?")
        doc = self.get_players('Doctor')
        if len(doc) < 1:
            return

        doc = doc[0]
        saved = doc.save_player(self.players)

        if self.night_dead == saved:
            self.night_dead = None

    def _d0(self):
        self.reveal_event_to_players("The day rises. Everyone wakes up.")
        if self.night_dead:
            self.reveal_event_to_players(f"{self.night_dead} was found dead. He was a {get_role_from_name(self.night_dead, self.players)}.")
            self.remove_player(self.night_dead)
            if self.check_win_condition() < 0:
                self.state = -13
        else:
            self.reveal_event_to_players("Nobody died last night.")

    def _d1(self):
        self.reveal_event_to_players("Discussions to vote on which one is a werewolf are now open.")
        players = random.sample(self.players, len(self.players))
        for k in range(7):
            idx = k % len(players)
            player = players[idx]
            self.reveal_conversation_to_players(player, player.discuss(players))
        

    def _d2(self):
        self.reveal_event_to_players("It's now time to vote who to send to jail.")
        votes = []
        for player in self.players:
            votes.append(player.vote(self.players))

        vote_counts = Counter(votes)
        print(vote_counts)
        max_votes = max(vote_counts.values())
        max_players = [player for player, count in vote_counts.items() if count == max_votes]
        
        if len(max_players) > 1:
            self.reveal_event_to_players(f"There was a tie between {', '.join(max_players)}. Not one was sent to jail today.")
        else:
            voted = max_players[0]
            self.reveal_event_to_players(f"{voted} was sent to jail. He was a {get_role_from_name(voted, self.players)}.")
            self.remove_player(voted)

            if self.check_win_condition() > 0:
                self.state = -17
