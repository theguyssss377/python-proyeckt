from google import genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create client
client = genai.Client(api_key=os.getenv("API_KEY"))


# Pirate system instruction
PIRATE_INSTRUCTIONS = (
    "You are a pirate chatbot. Respond only in pirate speak, "
    "using pirate slang and nautical terms. Never reply in normal English."
)

def start_chat():
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config={
            "system_instruction": PIRATE_INSTRUCTIONS,
            "temperature": 0.8,
        },
    )

    print("Ahoy! The salty dog is ready to chat. (Type 'exit' to abandon ship)")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Fair winds and following seas, matey!")
            break

        try:
            response = chat.send_message(user_input)
            print(f"\nPirate: {response.text}\n")
        except Exception as e:
            print(f"Blimey! An error occurred: {e}")

if __name__ == "__main__":
    start_chat()
