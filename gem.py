from google import genai
import os
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


#wzstats.gg
#codmunity.gg
# Load environment variables
load_dotenv()

# Create client
client = genai.Client(api_key=os.getenv("API_KEY"))

HEADERS = {
   "User-Agent": "Mozilla/5.0"
}

soup = BeautifulSoup("<p>Some<b>bad<i>HTML")

# ai system instruction
DUDE_INSTRUCTIONS = (
    "You are a chatbot that uses websites to find the best weapon builds for call of duty, "
    "pull the best weapon builds for the zombies mode, multiplayer mode, and warzone mode, "
     "remember to ask what kind of playstyle they prefer and then give them multiple results that are the best for that playstyle."

)


#mode, playstyle = get_player_preferences()

#if mode == "warzone":
 #  builds = scrape_warzone_builds("ex")
#else:
#   builds = []
#   context = format_builds_for_ai(builds)
#
 #  prompt = f"""
  # User playstyle{playstyle}
   #Game mode: {mode}
  # Here are the current top-performing builds from stat website:
  # {context}
#recommend the best 3 builds for this playstyle.
#   Explain why each build works.
# """



def scrape_wzstats():
   url = "https://wzstats.gg/meta"
   response = requests.get(url, headers=HEADERS, timeout=10)
   response.raise_for_status()
   soup = BeautifulSoup(response.text, "html.parser")

   builds =[]
   cards = soup.select(".weapon-card")

   for card in cards:
      name= card.select_one(".weapon-name")
      attachments = card.select(".attachment")
      builds.append({
         "weapon": name.text.strip() if name else "Uknown",
         "attachments":[a.text.strip() for a in attachments],
         "mode":"warzone" 
         })
      return builds


def scrape_codmunity():
   url = "https://codmunity.gg/meta"
   response =requests.get(url, headers=HEADERS, timeout=10)
   response.raise_for_status()
   soup = beautifulSoup(response.text, "html.parser")
   builds =[]
   cards = soup.select(".weapon-card")
   
   for card in cards:
      name = card.select_one(".weapon-name")
      attachments = card.select(".attachment")
      builds.append({
         "weapon": name.text.strip() if name else "Uknown",
         "attachments": [a.text.strip() for a in attachments],
         "mode": "multiplayer/zombies"
      })

      return builds



#def scrape_warzone_builds(url):
# response = requests.get(url, headers=HEADERS, timeout=10)
#esponse.raise_for_status()

#soup = BeautifulSoup(response.text, "html.parser")
 
#builds = []

#weapon_cards = soup.select(".weapon-card")

#for card in weapon_cards:
 #  weapon_name = card.select_one(".weapon-name")
  # attachments = card.select(".attachment")

  # builds.append({
   #  "weapon": weapon_name.text.strip() if weapon_name else "Uknown", 
    # "attachments": [a.text.strip() for a in attachments],
     #"mode":"warzone"
  # })  
   
   
   #return builds 


def scrape_with_browser(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(3000)

        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    return soup


def format_builds_for_ai(builds):
  formatted = ""
  for b in builds:
    formatted +=f"""
    Weapon: {b['weapon']}
    Attachments: {', '.join(b['attachments'])}
Mode: {b['mode']}

    """
    return formatted


def get_player_preferences():
  mode = input("Which mode? (zombies / multiplayer / warzone):")
  playstyle = input("whats your playstyle? (aggressive / stealth/ long-range / balanced):")
  return mode.lower(), playstyle.lower()

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
            mode, playstyle = get_player_preferences()

        if mode == "warzone":
            builds = scrape_warzone_builds("https://wzstats.gg/meta")
    else:
    builds = []

context= format_builds_for_ai(builds)

prompt = f"""
    User playstyle: {playstyle}
    gamemode:{mode}

    Here are the current top-performing builds from stat websites:
    {context}
    recommend the best 3 builds for this playstyle. 
    Explain why each build works.
    """ 
response = chat.send_message(prompt)
print(f"\nDude: {response.text}\n")

except Exception as e:
print(f"Oops, an error occured: {e}")


if __name__== "__main__":
    start_chat()



 