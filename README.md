# 🌿 Natuurpunt Vlaams-Brabant — Calendar Feed

An agentic AI script that automatically scrapes activities from [Natuurpunt Vlaams-Brabant](https://www.natuurpunt.be/agenda?f%5B0%5D=province%3A187) and converts them into a calendar file (`.ics`) you can import into Google Calendar, Apple Calendar, or Outlook.

## How does it work?

The script is an **AI agent**: you run it, and Claude (Anthropic's AI) does the rest. It:

1. Visits the Natuurpunt website
2. Analyzes the HTML structure
3. Writes its own code to parse the events
4. Generates an `.ics` calendar file
5. Remembers what worked for the next run

You don't write any scraping code — the agent figures it out on its own.

## Setup

You need Python 3.9+ and an [Anthropic API key](https://console.anthropic.com/).

```bash
# Clone the repo
git clone https://github.com/YOURUSERNAME/natuurpunt-calendar.git
cd natuurpunt-calendar

# Create a virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set your API key
export ANTHROPIC_API_KEY="sk-ant-..."
```

To avoid setting the API key every time, add the export line to your `~/.zshrc` and run `source ~/.zshrc`.

## Usage

### Run the agent

```bash
source venv/bin/activate
python natuurpunt_agenda.py
```

The agent creates `natuurpunt_vlaams_brabant.ics`. Double-click it to import into your calendar app.

### Run and publish to GitHub Pages

```bash
source venv/bin/activate
./run_and_publish.sh
```

This runs the agent and pushes the updated `.ics` to GitHub Pages so calendar subscriptions auto-update.

### Subscribe to the calendar

Instead of importing the `.ics` manually each time, you can subscribe to it so your calendar updates automatically. After publishing to GitHub Pages, your calendar URL is:

```
https://YOURUSERNAME.github.io/natuurpunt-calendar/natuurpunt_vlaams_brabant.ics
```

- **Google Calendar:** Other calendars → + → From URL → paste the URL
- **Apple Calendar:** File → New Calendar Subscription → paste the URL
- **Outlook:** Add calendar → Subscribe from web → paste the URL

### Automatic weekly updates

Add a cron job so the calendar updates itself:

```bash
crontab -e
```

Add this line (runs every Monday at 8am):

```
0 8 * * 1 cd /path/to/natuurpunt-calendar && source venv/bin/activate && ./run_and_publish.sh >> agent.log 2>&1
```

## Files

| File | What does it do? |
|---|---|
| `natuurpunt_agenda.py` | The AI agent |
| `run_and_publish.sh` | Runs the agent and pushes to GitHub Pages |
| `requirements.txt` | Python dependencies |
| `index.html` | Landing page with subscription instructions |
| `agent_notes.json` | Agent memory (created automatically after first run) |
| `natuurpunt_vlaams_brabant.ics` | Calendar file (created automatically) |

## Cost

The agent uses the Anthropic API (pay-per-use). A typical run costs $0.05–$0.30. After the first run, the agent remembers what worked, making subsequent runs faster and cheaper.

## Disclaimer

Not affiliated with [Natuurpunt vzw](https://www.natuurpunt.be). All data comes from the public Natuurpunt calendar.
