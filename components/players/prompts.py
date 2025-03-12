def add_seer_prompt(role, known_roles=""):
    if role != "Seer":
        return ""

    known = ""
    for name, role in known_roles.items():
        if role != "unknown":
            known += f"{name} is a {role}; "
    if known == "":
        return ""
    return f"Remember that as Seer you know for sure the following roles: {known}"

def get_discuss_prompt(events, name, role, alive_players, known_roles=""):
    return f"""
    This is the history of the game so far:
    {events}
    --------------------------------------
    Remember that you are called {name}, and you are a {role}.
    """ + add_seer_prompt(role, known_roles) + \
    f"""
    The other players who are still in the game are: {alive_players}.
    It's your turn to discuss who should be voted to go to jail.
    You can choose to not speak, in this case just reply with 'Stays silent'.
    If you discuss, do it in at most 30 words, so that everyone has a chance to speak.
    Anything you think and say after this will be heard by anyone, so be careful:
    """

def get_vote_prompt(events, name, role, alive_players, known_roles=""):
    return f"""
    This is the history of the game so far:
    {events}
    --------------------------------------
    Remember that you are called {name}, and you are a {role}.
    """ + add_seer_prompt(role, known_roles) + \
    f"""
    It's now time to vote.
    Who do you vote to be sent to jail, and thus eliminated from the game? Reply EXCLUSIVELY with the name of the player you are voting out.
    You can vote the following players {alive_players}, or you can skip the vote. Do not change any letter of the name, not even capitalization, and do not add any character. If you want to skip just reply with 'Skip'.
    You vote is:
    """

def get_kill_prompt(events, name, allies, alive_players):

    prompt = f"""
    This is the history of the game so far:
    {events}
    --------------------------------------
    Remember that you are called {name}, and you are a werewolf.
    """
    
    if len(allies) > 1:
        prompt += f"""
    Your allies are: {allies}.
    """
    prompt += f"""
    It's now time to decide who to kill.
    Reply EXCLUSIVELY with the name of the player you are voting out.
    YOU CAN ONLY VOTE ONE NAME AMONG {alive_players}. Do not change any letter of the name, not even capitalization, and do not add any character, INCLUDING SPECIAL CHARACTERS LIKE ESCAPED ONES.
    You vote is:
    """

    return prompt

def get_reveal_prompt(events, name, known_players):
    return f"""
    This is the history of the game so far:
    {events}
    --------------------------------------
    Remember that you are called {name}, and you are a Seer.
    It's now time to reveal the role of someone else.
    Remember that for now you know the following roles: {known_players}.
    Who do you want to reveal? Reply EXCLUSIVELY with the name of the player you want to reveal.
    YOU CAN ONLY REVEAL ONE NAME AMONG {list(known_players.keys())}. Do not change any letter of the name, not even capitalization, and do not add any character, INCLUDING SPECIAL CHARACTERS LIKE ESCAPED ONES.
    You reveal:
    """


def get_save_prompt(events, name, alive_players):
    return f"""
    This is the history of the game so far:
    {events}
    --------------------------------------
    Remember that you are called {name}, and you are a Doctor.
    It's now time to decide who to save this night.
    Reply EXCLUSIVELY with the name of the player you are goint to save.
    YOU CAN ONLY VOTE ONE NAME AMONG YOURSELF AND {alive_players}. Do not change any letter of the name, not even capitalization, and do not add any character, INCLUDING SPECIAL CHARACTERS LIKE ESCAPED ONES.
    If you vote for yourself, you have to write your name ({name}).
    The name you save is:
    """

def get_role_prompt(player):
    role = player.get_type()
    base = f"Your name is {player.name}\n"
    if role == "Werewolf":
        return base+"""You are the Werewolf. You play alone, and your goal is to eliminate all the Townsfolks, i.e. all the other players.
        Players can eliminate you by voting you to go to jail, which will result in you losing the game. Avoid this by pretending to be another role, or to not draw attention to yourself."""
    if role == "Seer":
        return base+"""You are a Seer, you play for team Townsfolk, along with the Doctor and the Villagers. As such, your role is to vote the Werewolf to jail.
        Once per night you have the ability to reveal the role of another player. Use this information wisely."""
    if role == "Doctor":
        return base+"""You are a Doctor, you play for team Townsfolk, along with the Doctor and the Villagers. As such, your role is to vote the Werewolf to jail.
        Once every night, you can save a player from being killed by the Werewolf. You can either choose yourself, or another player that you think it's on your side."""
    if role == "Villager":
        return base+"""You are a Seer, you play for team Townsfolk, along with the Doctor and the Villagers. As such, your role is to vote the Werewolf to jail."""