# Werewolf LLM Game

A text-based Werewolf game where different LLM models play against each other, with a visual replay system.

## Game Overview

This is a Werewolf game implementation where different LLM models take on roles like Werewolf, Villager, Seer, and Doctor. The game simulates the classic social deduction game where players must identify and eliminate the werewolves before they eliminate the townsfolk.

## Prerequisites

- Python 3.x
- Pygame (for visualization)
- Required Python packages (install via `pip install -r requirements.txt`)
- OpenRouter API key
- ElevenLabs API key (for text-to-speech)

## Installation

1. Clone the repository:
```bash
git clone git@github.com:giteliot/werewolf_llm.git
cd werewolf_llm
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

4. Set up your environment variables:
   - Set the following environment variables in your shell:
     ```bash
     export OR_KEY=your_openrouter_key
     export EL_KEY=your_elevenlabs_key
     ```
   - On Windows, use:
     ```cmd
     set OR_KEY=your_openrouter_key
     set EL_KEY=your_elevenlabs_key
     ```
   - You can get API keys from:
     - [OpenRouter](https://openrouter.ai/) for LLM access
     - [ElevenLabs](https://elevenlabs.io/) for text-to-speech

## Project Structure

```
werewolf_llm/
├── components/
│   ├── game.py         # Core game logic
│   ├── players/        # Player implementations
│   └── llm/           # LLM model configurations
├── visual/
│   └── viz.py         # Visualization system
├── run.py             # Game simulation runner
└── results/           # Directory for game logs
```

## Running the Game

### 1. Game Simulation

To run the game simulation:

```bash
python run.py
```

The simulation will make a single run with the all the roles chosen at random, and where you play your turn by writing text on your terminal.

### 2. Visual Replay

To visualize a game replay:

```bash
python visual/viz.py <path_to_game_log>
```

For example:
```bash
python visual/viz.py ./results/20240321_123456.txt
```

## Game Rules

- The game alternates between night and day phases
- During night:
  - Werewolves choose a victim
  - Seer can reveal a player's role
  - Doctor can save one player
- During day:
  - Players discuss and vote to eliminate a suspect
  - Game ends when either all werewolves or all townsfolk are eliminated

## Output

Game logs are saved in the `results/` directory with timestamps in the filename format: `YYYYMMDD_HHMMSS.txt`

