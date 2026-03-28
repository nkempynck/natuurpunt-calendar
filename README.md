# 🌿 Natuurpunt Vlaams-Brabant — Calendar Feed

An automatically updated calendar of [Natuurpunt Vlaams-Brabant](https://www.natuurpunt.be/agenda?f%5B0%5D=province%3A187) activities that you can subscribe to in Google Calendar, Apple Calendar, or Outlook.

Built with the [selfhealing-agent](https://github.com/nkempynck/selfhealing-agent) package — an AI agent that writes, runs, and fixes scripts using Claude.

## How does it work?

There are two modes:

- **`scrape_natuurpunt.py`** — A standalone scraper that fetches events and generates the calendar file. This is what runs on a schedule. No LLMs, no token usage, no API key, no cost.

- **`run.py`** — The entry point that ties it together. It tries the standalone script first. If it fails (e.g. the website changed), it fires up the AI agent to fix it. The agent reads the broken script, understands the issue, rewrites it, and saves the new version.

The agent is the fallback. The standalone script is what actually runs day-to-day.

### Regular workflow (scheduled updates)

1. A cron job runs `python run.py` every two weeks
2. `run.py` executes `scrape_natuurpunt.py` — no AI, no cost
3. The script scrapes the latest events and generates `natuurpunt_vlaams_brabant.ics`
4. The updated file is pushed to GitHub Pages
5. Your calendar subscription picks up the changes automatically

### When things break

1. `run.py` detects that `scrape_natuurpunt.py` failed
2. It fires up the AI agent (requires API key)
3. The agent reads the current script and your edits, figures out what changed, and fixes it
4. It saves the fixed script and notes for future reference

## Setup

You need Python 3.9+ and an [Anthropic API key](https://console.anthropic.com/) (only needed when the agent runs).

### Using conda/mamba

```bash
# Clone the repo
git clone https://github.com/nkempynck/natuurpunt-calendar.git
cd natuurpunt-calendar

# Create a conda environment
conda create -n natuurpunt python=3.11 -y
conda activate natuurpunt

# Install dependencies
pip install -r requirements.txt

# Set your API key (only needed if the agent has to run)
export ANTHROPIC_API_KEY="sk-ant-..."
```

If you prefer mamba:

```bash
mamba create -n natuurpunt python=3.11 -y
mamba activate natuurpunt
pip install -r requirements.txt
```

To avoid setting the API key every time, add the export line to your `~/.zshrc` and run `source ~/.zshrc`.

## Usage

### Run everything (script first, agent as fallback)

```bash
conda activate natuurpunt
python run.py
```

### Just run the standalone script (no agent fallback)

```bash
conda activate natuurpunt
python scrape_natuurpunt.py
```

### Force the agent to re-explore from scratch

```bash
conda activate natuurpunt
python -c "from run import agent; agent.run_agent_only()"
```

### Subscribe to the calendar

Subscribe so your calendar updates automatically:

```
https://nkempynck.github.io/natuurpunt-calendar/natuurpunt_vlaams_brabant.ics
```

- **Google Calendar:** Other calendars → + → From URL → paste the URL
- **Apple Calendar:** File → New Calendar Subscription → paste the URL
- **Outlook:** Add calendar → Subscribe from web → paste the URL

### Automatic updates with cron

```bash
crontab -e
```

Add this line (runs on the 1st and 15th of each month at 8am):

```
0 8 1,15 * * cd /path/to/natuurpunt-calendar && eval "$(conda shell.bash hook 2>/dev/null)" && conda activate natuurpunt && python run.py && git add natuurpunt_vlaams_brabant.ics && git commit -m "Update calendar" && git push
```

## Files

| File | What does it do? |
|---|---|
| `run.py` | Entry point — runs script, falls back to agent if it fails |
| `scrape_natuurpunt.py` | Standalone scraper (auto-generated) — no API key needed |
| `requirements.txt` | Python dependencies |
| `index.html` | Landing page with subscription instructions |
| `memory/` | Agent notes and script version history |
| `natuurpunt_vlaams_brabant.ics` | The calendar file (auto-generated) |

## Cost

- **Standalone script:** Free. No API calls.
- **Agent (fallback):** Uses the Anthropic API. A run costs ~$0.05–$0.30. Only triggers when the standalone script fails.

## Disclaimer

Not affiliated with [Natuurpunt vzw](https://www.natuurpunt.be). All data comes from the public Natuurpunt calendar.