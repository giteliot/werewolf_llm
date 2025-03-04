def get_discuss_prompt(events, name, role, alive_players):
    return f"""
    This is the history of the game so far:
    {events}
    --------------------------------------
    Remember that you are called {name}, and you are a {role}.
    The other players who are still in the game are: {alive_players}.
    It's your turn to discuss who should be voted to go to jail.
    You can choose to not speak, in this case just reply with 'Stays silent'.
    If you discuss, do it in at most 30 words, so that everyone has a chance to speak.
    Anything you think and say after this will be heard by anyone, so be careful:
    """

def get_vote_prompt(events, name, role, alive_players):
    return f"""
    This is the history of the game so far:
    {events}
    --------------------------------------
    Remember that you are called {name}, and you are a {role}.
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