from google import genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create client
client = genai.Client(api_key=os.getenv("API_KEY"))


# ai system instruction
DUDE_INSTRUCTIONS = (
    "You are a chatbot that uses websites to find the best weapon builds for call of duty, "
    "pull the best weapon builds for the zombies mode, multiplayer mode, and warzone mode, "
     "remember to ask what kind of playstyle they prefer and then give them multiple results that are the best for that playstyle."

)

def start_chat():
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config={
            "system_instruction": DUDE_INSTRUCTIONS,
            "temperature": 0.8,
        },
    )

    print("Whats up! Ready to chat? (Type 'exit' to leave the chat)")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("See you later!")
            break

        try:
            response = chat.send_message(user_input)
            print(f"\nDude: {response.text}\n")
        except Exception as e:
            print(f"Oops, an error occurred: {e}")

if __name__ == "__main__":
    start_chat()
