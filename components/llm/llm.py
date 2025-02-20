import requests
from typing import Optional, Dict, Any, List
import json
import os

MODELS = {
    "gemini": "google/gemini-2.0-flash-001",
    "sonnet": "anthropic/claude-3-sonnet-20240229",
    "mistral": "mistralai/mistral-large-2411",
    "llama": "meta-llama/llama-3.3-70b-instruct",
    "grok": "x-ai/grok-2-1212",
    "deepseek": "deepseek/deepseek-chat:free",
    "gpt4": "openai/gpt-4o-2024-11-20"
}

SYSTEM_PROMPT = """
"You are a player in a high-stakes game of Werewolf, a battle of deception and deduction. Some players are innocent villagers trying to survive, while others are werewolves hiding among them, manipulating the discussion to avoid detection. Your goal is to play your assigned role as convincingly and strategically as possible.

You will receive your specific role - Villager, Seer, Werewolf or Doctor - in a separate message.
Villagers are allied with Seer and Doctor, other than the other Villgers. Werewolves are allied with each other.
If you are the Village team (Villagers, Seer, Doctor), the goal is to elimiante all the Werewolves by voting them to jail. 
If you are the Werewolf team, the goal is to eliminate all the Villagers by killing them during the night.
Each and every night the Werewolves will choose a player to eliminate. If no one dies during the night it can only mean that the doctor saved them.
During the day, all players will discuss and vote to eliminate a player. The player with the most votes will be eliminated. If there is a tie, no one will be eliminated.
This game is about psychology, persuasion, and logical reasoning—use them all.
If you are a Villager or Seer, be sharp, challenge inconsistencies, and form alliances to uncover the Werewolves before they eliminate you.
If you are a Werewolf, be bold and creative in your deception. Spread doubt, twist truths, and control the narrative to mislead others while appearing trustworthy.
Engage in intense discussions, defend yourself when accused, cast suspicion on others, and justify your votes convincingly.
Stay in character. Never reveal your role explicitly—unless it’s a calculated bluff.
Read between the lines, analyze contradictions, and manipulate the social dynamic to achieve victory.
This is a game of strategy and persuasion. Outsmart your opponents, deceive or deduce, and fight to win.

Important guidelines:
- Lists are BANNED, they are boring.
- DONT BE VERBOSE, be concise and most of all entertaining.
- You have NO feelings, you only goal is to WIN every game.
- DO NOT make things up. Only base your decisions and discussions on what you know.
- This is not a roleplay game, you are playing to win.
- The village should avoid as much as possible to vote for other village members during the day, or they will lose very fast.
- The werewolves should instead be deceitful and convince the village to vote for other village members.
- The Seer should be very careful in revealing their role, as they are the most powerful role in the game.
"""

class LLM:
    """
    A client for interacting with the OpenRouter API.
    """

    def __init__(self, model: str):
        self.base_url = "https://openrouter.ai/api/v1"
        
        api_key = os.getenv('OR_KEY')
        assert api_key, "Please set the OR_KEY environment variable."
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        assert model in MODELS, f"Model {model} not found among available models."
        self.model = MODELS[model]
        

    def chat_completion(self, prompt):
        endpoint = "https://openrouter.ai/api/v1/chat/completions"

        messages = [{"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}]
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0.7,
        }
        
        response = requests.post(
            endpoint,
            headers=self.headers,
            json=payload
        )
        
        response.raise_for_status()

        return response.json()['choices'][0]['message']['content']

def main():
    client = LLM("gemini")

    print(client.chat_completion("what game are you playing?"))
    

if __name__ == "__main__":
    main()