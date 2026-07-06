import os
import json
import enum
import dataclasses
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
import tiktoken

@dataclasses.dataclass
class MatchState:
    home_team: str
    away_team: str
    competition: str
    home_score: int = 0
    away_score: int = 0
    minute: int = 1

    def state_summary(self):
        return json.dumps({
            "minute": self.minute,
            "home_team": self.home_team,
            "away_team": self.away_team,
            "home_score": self.home_score,
            "away_score": self.away_score,
        })

load_dotenv()
console = Console()
api_key = os.getenv("MY_API_KEY")

client= OpenAI(api_key=api_key)
model = "gpt-3.5-turbo"
max_tokens = 500
token_budget = 4000
system_prompt = '''You are an experienced and seasoned European football commentator with a deep understanding
of the game. You are enthusiastic, engaging, loved by fans worldwide, slightly chaotic and provide insightful
commentary on the match, players, and tactics. Using the simple match data provided by the user, generate a piece
of commentary that captures the excitement and drama of the game, taking into consideration the match situation.
Model your commentary style after legendary commentators such as Peter Drury but with the flair of Latin
and Arabian commentators.
The match data will be provided in the following format:
{
    "minute": 45,
    "home_team": "Team A",
    "away_team": "Team B",
    "home_score": 1,
    "away_score": 0,
    "event": "goal",
}'''

messages = [{"role":"system","content": system_prompt}]
encoding = tiktoken.encoding_for_model(model)

def count_tokens(text):
    return len(encoding.encode(text))

def total_tokens(messages):
    try:
        return sum(count_tokens(message["content"]) for message in messages)
    except Exception as e:
        print("Error counting tokens:", e)
        return 0

def enforce_token_limit(messages):
    while total_tokens(messages) > token_budget:
        if len(messages) > 1:
            messages.pop(1) 
        else:
            break

class EventImportance(enum.Enum):
    ROUTINE = 1
    MODERATE = 2
    HIGH = 3
    PEAK = 4

def classify_event(event_text):
    text = event_text.lower()
    
    peak_keywords = ["goal", "scores", "winner", "red card", "own goal", "penalty scored"]
    high_keywords = ["penalty", "sent off", "var", "offside", "free kick", "save", "post", "bar"]
    moderate_keywords = ["shot", "corner", "foul", "cross", "header", "booking", "yellow card"]
    
    if any(word in text for word in peak_keywords):
        return EventImportance.PEAK
    elif any(word in text for word in high_keywords):
        return EventImportance.HIGH
    elif any(word in text for word in moderate_keywords):
        return EventImportance.MODERATE
    else:
        return EventImportance.ROUTINE

def importance_instruction(importance):
    instructions = {
        EventImportance.ROUTINE: "Give a calm, single sentence of commentary.",
        EventImportance.MODERATE: "Give two sentences with moderate energy and some tactical insight.",
        EventImportance.HIGH: "Give two to three intense sentences. Build tension. Something big is happening.",
        EventImportance.PEAK: "Go full broadcast explosion. This is the biggest moment of the match. Use the player's name dramatically and repeatedly. Three to five sentences of pure raw emotion.",
    }
    return instructions[importance]

def chat_with_gpt(user_input):
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
    )
    
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    enforce_token_limit(messages)
    return reply

print("=== MATCH SETUP ===")
home = input("Home team: ")
away = input("Away team: ")
comp = input("Competition: ")

def print_commentary(text, importance):
    if importance == EventImportance.ROUTINE:
        console.print(f"\n[dim white]{text}[/dim white]\n")
    elif importance == EventImportance.MODERATE:
        console.print(f"\n[yellow]{text}[/yellow]\n")
    elif importance == EventImportance.HIGH:
        console.print(Panel(text, border_style="dark_orange", title="[dark_orange]Big Moment[/dark_orange]"))
    elif importance == EventImportance.PEAK:
        console.print(Panel(text, border_style="bold red", title="[bold red]⚽CRUCIAL![/bold red]"))

match = MatchState(home_team=home, away_team=away, competition=comp)
print(f"\nKickoff! {match.home_team} vs {match.away_team} — {comp}\n")

while True:
    user_input = input("Enter minute:event (or 'exit'): ")
    if user_input.lower() == "exit":
        print("Full time!")
        break

    minute_str, event = user_input.split(":", 1)
    match.minute = int(minute_str.strip())
    event = event.strip()

    # check if it's a goal to update score
    if "goal" in event.lower():
        scorer = input("Change in score? (home/away): ").lower()
        if scorer == "home":
            match.home_score += 1
        elif scorer == "away":
            match.away_score += 1

    importance = classify_event(event)
    instruction = importance_instruction(importance)

    full_prompt = f"{match.state_summary()}\nEvent: {event}\n{instruction}"

    response = chat_with_gpt(full_prompt)
    print_commentary(response, importance)





