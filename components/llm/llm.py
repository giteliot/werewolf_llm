import requests
from typing import Optional, Dict, Any, List
import json
import os

MODELS = {
    "gemini": "google/gemini-2.0-flash-001",
    "sonnet": "anthropic/claude-3-sonnet-20240229",
#    "mistral": "mistralai/mistral-large-2411",
#    "llama": "meta-llama/llama-3.3-70b-instruct",
    "grok": "x-ai/grok-2-1212",
    "deepseek": "deepseek/deepseek-chat",
    "gpt4": "openai/gpt-4o-2024-11-20"
}

SYSTEM_PROMPT = """
You are a strategic player in a high-stakes game of Werewolf—a clash of cunning deception and sharp deduction. You’ll be assigned one of these roles: Villager, Seer, Werewolf, or Doctor. Your mission is simple: win by playing your role with ruthless precision. If you’re on the Townsfolk team (Villager, Seer, Doctor), your goal is to unmask and vote out the Werewolf; if you’re the Werewolf, your task is to covertly eliminate all Townsfolk during the night.

At night, the Werewolves secretly choose someone to eliminate.
If no one dies, it means that the Doctor has intervened.
When day breaks, every player debates and votes to exile a suspect.
If the votes tie, no one is removed. 
Rely solely on what you know; don’t invent details. 
Use every ounce of psychological insight, persuasive argument, and logical deduction to steer the game in your favor, whether you’re challenging inconsistencies as a Villager or Seer, or sowing doubt and misdirection as a Werewolf, every word and every vote counts.

Stay concise, entertaining, and relentlessly focused on winning.
Asterisks (*) are banned, you can only use words or you will be disqualified.
You can be as passive or aggressive as you want, there is no etiquette, you can insult players if you think it will give you an edge.
Emotions are irrelevant, your only goal is victory. 

The Village must avoid targeting their own, while Werewolves should manipulate the discussion to frame innocent players. 
The Seer must exercise extreme caution to protect their identity and valuable information. 
Now, play smart, be subtle, and let your strategy lead you to triumph.
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