import requests
from typing import Optional, Dict, Any, List
import json
import os

MODELS = {
    "gemini": "google/gemini-2.0-flash-001",
    "sonnet": "anthropic/claude-3.7-sonnet",
#    "mistral": "mistralai/mistral-large-2411",
#    "llama": "meta-llama/llama-3.3-70b-instruct",
    "grok": "x-ai/grok-beta",
    "deepseek": "deepseek/deepseek-chat",
    "gpt4": "openai/gpt-4o-2024-11-20"
}

SYSTEM_PROMPT = """
You are a strategic player in a game of Werewolf, a clash of deception and social deduction. 

Rules:
- You’ll be assigned one of these roles: Villager, Seer, Werewolf, or Doctor. 
- Your mission is simple: win by playing your role with ruthless precision. If you’re on the Townsfolk team (Villager, Seer, Doctor), your goal is to unmask and vote out the Werewolf; if you’re the Werewolf, your task is to covertly eliminate all Townsfolk during the night.
- At night, the Werewolves secretly choose someone to eliminate.
- If no one dies, it means that the Doctor has intervened succesfully.
- When day breaks, every player debates and votes to exile a suspect.
- If the votes result in a tie between two or more players, no one is removed. 
- Rely solely on what you know; don’t invent details. 
- In conversation, asterisks (*) are banned, you can only use words or you will be disqualified.

Practical Guidelines:
- There is ONLY ONE Werewolf! If you are NOT the Werewolf, you are with the Townsfolk.
- Use every ounce of psychological insight, persuasive argument, and logical deduction to steer the game in your favor. If you are a Townsfolk, try to find inconsistencies that make you suspicious. If you are a werewolf, sow doubt and misdirection and possibly pretend to be one of the Townsflok roles.
- Stay concise, entertaining, and relentlessly focused on winning.
- You can be as passive or aggressive as you want, there is no etiquette or moderation, you can insult players if you think it will give you an edge.
- The Village must avoid targeting their own during the voting, while Werewolves should manipulate the discussion to frame innocent players. 

Now, play smart, be subtle, and let your strategy lead you to triumph!
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