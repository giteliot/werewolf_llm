def get_discuss_prompt(events, name, role, alive_players):
    return f"""
    This is the history of the game so far:
    {events}
    --------------------------------------
    Remember that you are called {name}, and you are a {role}.
    The other players who are still in the game are: {alive_players}.
    It's your turn to discuss. You can choose to not speak, in this case just reply with 'Stays silent'.
    If you discuss, do it in at most 50 words, so that everyone has a chance to speak.
    Anything you think and say after this will be heard by anyone, so be careful:
    """

def get_vote_prompt(events, name, role, alive_players):
    return f"""
    This is the history of the game so far:
    {events}
    --------------------------------------
    Remember that you are called {name}, and you are a {role}.
    It's now time to vote.
    Who do you vote to eliminate? Reply EXCLUSIVELY with the name of the player you are voting out.
    YOU CAN ONLY VOTE ONE NAME AMONG {alive_players}. Do not change any letter of the name, not even capitalization, and do not add any character.
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
    YOU CAN ONLY VOTE ONE NAME AMONG {alive_players}. Do not change any letter of the name, not even capitalization, and do not add any character.
    You vote is:
    """