"""
Natuurpunt Vlaams-Brabant Calendar Agent
========================================
Uses the selfhealing-agent package to scrape Natuurpunt events
and generate an .ics calendar file.

First run:  Claude explores the website and writes scrape_natuurpunt.py
Next runs:  Runs scrape_natuurpunt.py directly (no API cost)
If broken:  Agent takes over, reads your script, fixes it

Usage:
    pip install git+https://github.com/nkempynck/selfhealing-agent.git
    export ANTHROPIC_API_KEY="sk-ant-..."
    python run.py
"""

from selfhealing_agent import Agent

agent = Agent(
    name="natuurpunt-calendar",
    instructions="""\
You are an autonomous web scraping agent. Your task is to:

1. Fetch the Natuurpunt agenda page (https://www.natuurpunt.be/agenda)
2. Inspect the HTML to understand the page structure
3. Figure out how to filter or find events for the province "Vlaams-Brabant".
4. Write and execute Python code that:
   - Parses the events (title, date, time, location, description, URL). \
ONLY FIND FUTURE OR CURRENT EVENTS, NOT PAST ONES.
   - Filters for Vlaams-Brabant events. They can be found under this URL: \
https://www.natuurpunt.be/agenda?f%5B0%5D=province%3A187&page=1
   - Add event information to an .ics calendar file using the icalendar \
library. I'd basically like to see the information from the website in \
calendar form, so I can import it into Google Calendar or Apple Calendar. \
The calendar should be timezone-aware (Europe/Brussels) and handle Dutch \
date formats.
   - Make sure to find the actual time of the event, not just the date. \
It is found in the link of the event (example: \
https://www.natuurpunt.be/agenda/mijmerende-meanderwandeling-aansluitend-\
lokale-algemene-leden-vergadering-26239?date=29/03/2026). \
If the time is not specified, default to 10:00 AM. But really try to find \
the time, because some events do have it and it would be a shame to lose \
that information.
   - Make sure to check all the pages, not just the first one. The \
pagination is found at the bottom of the page, and it is in the form of a \
list of page numbers (1, 2, 3, ...). You can find the URL for each page \
by changing the "page" parameter in the URL.
   - Generates an .ics calendar file saved as 'natuurpunt_vlaams_brabant.ics'. \
Ensure the events are not from the past. Only include current and future \
events. Otherwise restart.
   - Print out the number of events found and included in the calendar. And \
some example events with their title and date, so I can verify it worked. \
If no events are found, print a warning and restart the process. If you \
only checked the first page and have events for only the recent future, \
you also failed. You need to check multiple pages.

Strategy:
- Start by fetching the Vlaams-Brabant filtered agenda page to see the \
HTML structure: https://www.natuurpunt.be/agenda?f%5B0%5D=province%3A187
- If the page is JavaScript-rendered (fetch_url returns empty/minimal \
content), try fetch_url_selenium
- Once you understand the HTML structure, write Python code to parse it \
and generate the .ics file
- Handle Dutch date formats (e.g., "za 12 april 2025", "12/04/2025")
- Set timezone to Europe/Brussels
- If your code fails, read the error and fix it
""",
    output_file="natuurpunt_vlaams_brabant.ics",
    script_file="scrape_natuurpunt.py",
)

if __name__ == "__main__":
    agent.run()