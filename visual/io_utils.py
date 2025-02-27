import sys

def load_game_log(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip().replace('""', '"').split(":", 1) for line in file if line.strip() if len(line) > 5][:-6]
    except FileNotFoundError:
        print(f"Error: Could not find log file at {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading log file: {e}")
        sys.exit(1)