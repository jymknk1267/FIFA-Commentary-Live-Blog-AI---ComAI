# ComAI 🎙️⚽

A context-aware AI football commentary engine that generates broadcast-quality, emotionally calibrated commentary from live match events. Type a match event, get Peter Drury-level drama back instantly — scaled to the moment.

---

## How It Works

1. User sets up the match — teams, competition, and starting conditions
2. Each event is entered in natural language alongside the current minute
3. A keyword-based classification engine assigns the event an importance tier (Routine → Moderate → High → Peak)
4. A prompt is dynamically constructed combining the real-time match state (score, minute, teams, competition) with a tier-specific instruction and a persona-driven system prompt
5. GPT-3.5 Turbo generates commentary calibrated to the emotional weight of the moment
6. Output is styled in the terminal using Rich — from dim prose for routine play to bold red panels for goals

---

## Project Structure

```
├── main.py           # Core application — match setup, event loop, commentary engine
├── .env              # API key (not committed)
├── .gitignore
└── requirements.txt
```

---

## Setup

**1. Clone the repository and create a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your OpenAI API key to `.env`**
```
OPENAI_API_KEY=your-key-here
```

**4. Run the commentator**
```bash
python main.py
```

---

## Example Session

```
=== MATCH SETUP ===
Home team: Argentina
Away team: France
Competition: FIFA World Cup 2022 Final

Kickoff! Argentina vs France — FIFA World Cup 2022 Final

Enter minute:event (or 'exit'): 23:Messi steps up and drives the penalty into the bottom corner
Which team scored? (home/away): home

╔══════════════════════════════════╗
║          ⚽ CRUCIAL!             ║
║                                  ║
║  MESSI! LIONEL MESSI! He doesn't ║
║  miss. He never misses when it   ║
║  matters most...                 ║
╚══════════════════════════════════╝
```

---

## Event Importance Tiers

| Tier | Keywords | Commentary Style |
|------|----------|-----------------|
| Routine | pass, run, dribble | Calm, single sentence |
| Moderate | shot, corner, foul, cross | Two sentences, tactical insight |
| High | penalty, VAR, free kick, save | Tense, two to three sentences |
| Peak | goal, scores, red card, own goal | Full broadcast explosion |

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| OpenAI API (GPT-3.5 Turbo) | Commentary generation |
| Rich | Terminal styling by importance tier |
| tiktoken | Token counting and context window management |
| python-dotenv | API key management |
