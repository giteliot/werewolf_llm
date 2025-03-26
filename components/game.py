from typing import List, Tuple
from .players.player import create_player, Player
from .players.prompts import get_role_prompt
import random
from collections import Counter
from components.players.utils import get_role_from_name

class Game:
    def __init__(self, players: List[Tuple[str, str, bool]]):
        self.players: List[Player] = [create_player(name, role, is_human) for name, role, is_human in players]
        self.state = 0
        self.night_dead = None
        self.logs = []

        self.state_handlers = {
            0: self._n0,
            1: self._n1,
            2: self._n2,
            3: self._d0,
            4: self._d1,
            5: self._d2
        }

        self._setup()
        self.first_round = True

    def _setup(self):
        self.reveal_event_to_players("A new game is beginning.")
        for player in self.players:
            player.events.append(get_role_prompt(player))
        for p1 in self.get_players('Werewolf'):
            for p2 in self.get_players('Werewolf'):
                if p1 != p2:
                    p1.events.append(f"{p2.name} is another Werewolf! You are allied in this game.")

    def _post_game(self, winner: str):
        for player in self.players:
            player.update_memory(self.players, winner)

    def get_players(self, role: str) -> List[Player]:
        return [player for player in self.players if player.__class__.__name__ == role]

    def remove_player(self, player_name: str):
        self.players = [player for player in self.players if player.name != player_name]

    def reveal_event_to_players(self, event_description):
        rich_text = f'Narrator: "{event_description}"'
        print()
        print(rich_text)
        self.logs.append(rich_text)

        for p in self.players:
            p.events.append(rich_text)

    def reveal_conversation_to_players(self, player, message):
        rich_text = f'{player.name}: "{message}"'
        print()
        print(rich_text)
        self.logs.append(rich_text)

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
            return 1

        if 2*len(werewolves) >= len(self.players):
            return -1
        
        return 0

    def _n0(self):
        if self.first_round == True:
            self.reveal_event_to_players("The night falls, and everyone goes to sleep.")
            return
        self.reveal_event_to_players("The night falls, and everyone goes to sleep. The werewolf wakes up and chooses his victim.")
        werewolf = random.sample(self.get_players('Werewolf'), 1)[0]
        dead = werewolf.kill_player(self.players)
        self.night_dead = dead

    def _n1(self):
        seer = self.get_players('Seer')
        if len(seer) < 1:
            return
        self.reveal_event_to_players("The Seer wakes up and chooses someone to reveal the role.")
        seer = seer[0]
        seer.reveal(self.players)

    def _n2(self):
        if self.first_round == True:
            return
        doc = self.get_players('Doctor')
        if len(doc) < 1:
            return
        self.reveal_event_to_players("The doctor wakes up and chooses someone to save.")
        doc = doc[0]
        saved = doc.save_player(self.players)

        if self.night_dead == saved:
            self.night_dead = None

    def _d0(self):
        if self.first_round == True:
            self.reveal_event_to_players("The sun rises, everyone wakes up and gather in the town square. Rumors have that a Werewolf was spotted last night. You need to find out who among you the werewolf is, before anyone gets killed.")
            self.first_round = False
            return
        self.reveal_event_to_players("The sun rises, everyone wakes up and gather in the town square.")
        if self.night_dead:
            self.reveal_event_to_players(f"{self.night_dead} was found dead. He was a {get_role_from_name(self.night_dead, self.players)}.")
            self.remove_player(self.night_dead)
            if self.check_win_condition() < 0:
                self.reveal_event_to_players("Werewolves win!")
                self.state = -13
                self._post_game("Werewolf")
        else:
            self.reveal_event_to_players("Nobody died last night. The doctor successfully saved the victim")

    def _d1(self):
        self.reveal_event_to_players("Now you can discuss who should be sent to jail.")
        players = random.sample(self.players, len(self.players))
        for k in range(5):
            idx = k % len(players)
            player = players[idx]
            self.reveal_conversation_to_players(player, player.discuss(players))
        

    def _d2(self):
        self.reveal_event_to_players("Time's up, it's now time to vote who you want to send to jail..")
        votes = []
        for player in self.players:
            target = player.vote(self.players)
            votes.append(target)
            self.reveal_conversation_to_players(player, target)

        vote_counts = Counter([vote for vote in votes if vote != 'Skip'])
        max_votes = max(vote_counts.values())
        max_players = [player for player, count in vote_counts.items() if count == max_votes]
        
        if len(max_players) > 1:
            self.reveal_event_to_players(f"There was a tie between {', '.join(max_players)}. Not one was sent to jail today.")
        else:
            voted = max_players[0]
            self.reveal_event_to_players(f"{voted} was sent to jail. He was a {get_role_from_name(voted, self.players)}.")
            self.remove_player(voted)

            if self.check_win_condition() > 0:
                self.reveal_event_to_players("Townsfolk win!")
                self.state = -17
                self._post_game("Townsfolk")
