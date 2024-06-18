from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

class ChatIAConnection:
    def get_chat_response(self, prompt):
        try:
            response = client.chat.completions.create(
                model="TheBloke/Mistral-7B-Instruct-v0.2-GGUF",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error fetching response from model: {e}")
            return str(e)

# Créer une instance globale pour pouvoir l'utiliser dans main.py
client_conn = ChatIAConnection()
