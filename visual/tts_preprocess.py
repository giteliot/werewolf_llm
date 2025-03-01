import requests
import json
import os
from const import BASE_TTS, voices
from utils import load_game_log
import hashlib
import sys

def generate_and_save_audio(text, voice_id, api_key, output_filename):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }
    
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            # Save the audio content to a file
            with open(output_filename, 'wb') as f:
                f.write(response.content)
            print(f"Audio saved to {output_filename}")
            return True
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            return False
            
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return False


def preprocess_audio(log_file_path):
    api_key = os.getenv('EL_KEY')
    assert api_key, "Eleven Labs API key not found. Please set the EL_KEY environment variable."

    game_log = load_game_log(log_file_path)
    
    for char, text in game_log:
        os.makedirs(f"{BASE_TTS}/{char}", exist_ok=True)
        text_hash = hashlib.md5(text.encode()).hexdigest()
        output_file = f"{BASE_TTS}/{char}/{text_hash}.mp3"
        if not os.path.exists(output_file):
            generate_and_save_audio(text, voices[char.lower()], api_key, output_file)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_game_log>")
        sys.exit(1)
    log_file_path = sys.argv[1]
    preprocess_audio(log_file_path)