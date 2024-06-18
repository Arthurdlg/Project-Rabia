# Example: reuse your existing OpenAI setup
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

class ChatIAConnection:
    def get_chat_response(self, prompt, temp=0.7, context='default'):
        try:
            system_content = "You are a helpful assistant."
            if context == 'search':
                system_content = "You respond only by yes or no and nothing else no more no less."
            response = client.chat.completions.create(
                model="TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": prompt}
                ],
                temperature=temp,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error fetching response from model: {e}")
            return str(e)

# Créer une instance globale pour pouvoir l'utiliser dans main.py
client_conn = ChatIAConnection()
