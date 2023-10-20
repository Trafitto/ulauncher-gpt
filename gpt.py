import requests
import json

OPEN_API_CHAT_URL =  'https://api.openai.com/v1/chat/completions'

class GPT:
    def __init__(self, ulauncer_preferences):
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ulauncer_preferences['OPENAI_API_KEY']}",
        }
        self.messages = [] # TODO: Add personality
        self.data = {
             "model": ulauncer_preferences['MODEL'],
            "temperature": int(ulauncer_preferences['TEMPERATURE'])
        }
        
    def ask(self, message: str) -> str:
        self.messages.append({"role": "user", "content": message})
        self.data['messages'] = self.messages
        response = requests.post(
            OPEN_API_CHAT_URL, headers=self.headers, data=json.dumps(self.data))

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")