import sys

def load_game_log(file_path):
    try:
        with open(file_path, 'r') as file:
            return [[l.strip().replace('""', '"').strip('"') for l in line.split(":", 1)] for line in file if line.strip() if len(line) > 5][:-6]
    except FileNotFoundError:
        print(f"Error: Could not find log file at {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading log file: {e}")
        sys.exit(1)

def load_final_results(file_path):
    with open(file_path, 'r') as file:
        res = [[l.strip() for l in line.split(":", 1)] for line in file][-6:]
    winner = res[0][1]
    townsfolks = []
    werewolves = []
    for name, role in res[1:]:
        if "werewolf" == role.lower():
            werewolves.append(name)
        else:
            townsfolks.append(name)
    return winner, townsfolks, werewolves

def get_eliminated_player(speaker, message):
    if speaker != "narrator":
        return None

    tokens = message.replace(".", "").split(" ")
    if "was found dead" in message:
        return (tokens[0].lower(), tokens[-1].lower(), "killed")

    if "was sent to jail" in message:
        return (tokens[0].lower(), tokens[-1].lower(), "jailed")
    