import os

def get_role_from_name(name, players):
    role = None
    for p in players:
        if p.name == name:
            role = p.get_type()
            break
    return role

def sanitize_name(name, players):
    name = name.lower()
    if "skip" in name:
        return "Skip"
    for p in players:
        if p.name in name:
            return p.name
    return None

def get_human_input(prompt):
    return input(prompt)

def load_file_content(player_name):
    try:
        with open(f"./data/{player_name}.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return ""
    
def save_file_content(player_name, text):
    os.makedirs("./data", exist_ok=True)
    
    with open(f"./data/{player_name}.txt", "w") as f:
        f.write(text)