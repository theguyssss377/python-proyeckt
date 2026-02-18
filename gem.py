from google import genai
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

load_dotenv()

client = genai.Client(api_key=os.getenv("API_KEY"))

DUDE_INSTRUCTIONS = (
    "You are a chatbot that finds the best Call of Duty weapon builds. "
    "Provide builds for zombies, multiplayer, and warzone. "
    "Ask their playstyle and recommend the best 3 builds."
)


# ---------------- PLAYWRIGHT SCRAPER ---------------- #

def scrape_with_browser(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(url, timeout=60000)
        page.wait_for_timeout(5000)  # wait for JS to load

        html = page.content()
        browser.close()

    return BeautifulSoup(html, "html.parser")


def scrape_wzstats():
    url = "https://www.wzstats.gg/meta"
    soup = scrape_with_browser(url)

    builds = []
    cards = soup.select(".weapon-card")

    for card in cards:
        name = card.select_one(".weapon-name")
        attachments = card.select(".attachment")

        builds.append({
            "weapon": name.text.strip() if name else "Unknown",
            "attachments": [a.text.strip() for a in attachments],
            "mode": "warzone"
        })

    return builds


def scrape_codmunity():
    url = "https://codmunity.gg/meta"
    soup = scrape_with_browser(url)

    builds = []
    cards = soup.select(".weapon-card")

    for card in cards:
        name = card.select_one(".weapon-name")
        attachments = card.select(".attachment")

        builds.append({
            "weapon": name.text.strip() if name else "Unknown",
            "attachments": [a.text.strip() for a in attachments],
            "mode": "multiplayer/zombies"
        })

    return builds


# ---------------- FORMAT ---------------- #

def format_builds_for_ai(builds):
    formatted = ""

    for b in builds:
        formatted += f"""
Weapon: {b['weapon']}
Attachments: {', '.join(b['attachments'])}
Mode: {b['mode']}

"""
    return formatted


# ---------------- USER INPUT ---------------- #

def get_player_preferences():
    mode = input("Which mode? (zombies / multiplayer / warzone): ")
    playstyle = input("Whats your playstyle? (aggressive / stealth / long-range / balanced): ")
    return mode.lower(), playstyle.lower()


# ---------------- CHAT ---------------- #

def start_chat():
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config={
            "system_instruction": DUDE_INSTRUCTIONS,
            "temperature": 0.8,
        },
    )

    print("Whats up! Ready to chat? (Type 'exit' to leave)")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("See you later!")
            break

        try:
            mode, playstyle = get_player_preferences()

            if mode == "warzone":
                builds = scrape_wzstats()
            else:
                builds = scrape_codmunity()

            if not builds:
                print("No builds found. Site structure may have changed.")
                continue

            context = format_builds_for_ai(builds)

            prompt = f"""
User playstyle: {playstyle}
Game mode: {mode}

Here are the current top-performing builds:
{context}

Recommend the best 3 builds for this playstyle.
Explain why each build works.
"""

            response = chat.send_message(prompt)
            print(f"\nDude: {response.text}\n")

        except Exception as e:
            print(f"Oops, an error occurred: {e}")


if __name__ == "__main__":
    start_chat()
