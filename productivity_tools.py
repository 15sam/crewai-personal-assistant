"""
productivity_tools.py
---------------------
Collection of CrewAI Tools:
1. SearchInternetTool  — Uses Google Custom Search API
2. ScrapeWebsiteTool   — Extracts readable text from a webpage
3. SendEmailTool       — Sends emails via Gmail SMTP
4. CreateCalendarEventTool — Creates Google Calendar events
"""

import os
import ssl
import smtplib
import requests
from typing import Type, List
from pydantic import BaseModel, Field
from bs4 import BeautifulSoup
from crewai.tools import BaseTool

# Google Calendar API imports
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


from duckduckgo_search import DDGS


# =========================================================
# 1️⃣  INTERNET SEARCH TOOL (DUCKDUCKGO)
# =========================================================

class DuckDuckGoSearchToolSchema(BaseModel):
    query: str = Field(..., description="Search query string")

class DuckDuckGoSearchTool(BaseTool):
    name: str = "DuckDuckGo Search Tool"
    description: str = "Search the internet using DuckDuckGo."
    args_schema: Type[BaseModel] = DuckDuckGoSearchToolSchema

    def _run(self, query: str) -> str:
        """Performs an internet search using DuckDuckGo."""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=5))
                if not results:
                    return "No search results found."

                formatted = "Search Results:\n\n"
                for i, item in enumerate(results, 1):
                    formatted += (
                        f"{i}. {item.get('title', 'No title')}\n"
                        f"   URL: {item.get('href', 'No URL')}\n"
                        f"   Snippet: {item.get('body', 'No description')}\n\n"
                    )
                return formatted.strip()

        except Exception as e:
            return f"Error performing search: {e}"

# =========================================================
# 2️⃣  WEB SCRAPER TOOL
# =========================================================

class ScrapeWebsiteToolSchema(BaseModel):
    url: str = Field(..., description="URL of the website to scrape")


class ScrapeWebsiteTool(BaseTool):
    name: str = "Scrape Website Tool"
    description: str = "Extracts text content from a given URL."
    args_schema: Type[BaseModel] = ScrapeWebsiteToolSchema

    def _run(self, url: str) -> str:
        """Scrapes website text content."""
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            for tag in soup(["script", "style"]):
                tag.decompose()

            text = soup.get_text(separator="\n")
            lines = (line.strip() for line in text.splitlines())
            cleaned = "\n".join(line for line in lines if line)

            if len(cleaned) > 5000:
                cleaned = cleaned[:5000] + "...\n[Content truncated]"

            return f"Content from {url}:\n\n{cleaned}"

        except Exception as e:
            return f"Error scraping website: {e}"


# =========================================================
# 3️⃣  EMAIL TOOL
# =========================================================

class SendEmailToolSchema(BaseModel):
    to: str = Field(..., description="Recipient's email address")
    subject: str = Field(..., description="Email subject line")
    body: str = Field(..., description="Email body content")


class SendEmailTool(BaseTool):
    name: str = "Send Email Tool"
    description: str = "Send an email using Gmail SMTP."
    args_schema: Type[BaseModel] = SendEmailToolSchema

    def _run(self, to: str, subject: str, body: str) -> str:
        """Send an email via Gmail SMTP."""
        sender = os.getenv("EMAIL_SENDER")
        password = os.getenv("EMAIL_PASSWORD")

        if not sender or not password:
            return "Error: EMAIL_SENDER or EMAIL_PASSWORD not set in .env file."

        message = f"Subject: {subject}\n\n{body}".encode("utf-8")
        context = ssl.create_default_context()

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender, password)
                server.sendmail(sender, to, message)
            return f"Email successfully sent to {to}."
        except smtplib.SMTPAuthenticationError:
            return "Error: SMTP Authentication failed. Please check your EMAIL_SENDER and EMAIL_PASSWORD in the .env file. You may need to use a Gmail App Password."
        except Exception as e:
            return f"Error sending email: {e}"


# =========================================================
# 4️⃣  GOOGLE CALENDAR TOOL
# =========================================================

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'


def _get_calendar_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"Missing '{CREDENTIALS_FILE}'. Download from Google Cloud Console."
                )
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return build('calendar', 'v3', credentials=creds)


class CreateCalendarEventToolSchema(BaseModel):
    summary: str = Field(..., description="Event title/summary")
    start_datetime_str: str = Field(..., description="Start datetime in ISO 8601 format (e.g. '2025-10-21T16:00:00')")
    end_datetime_str: str = Field(..., description="End datetime in ISO 8601 format (e.g. '2025-10-21T17:00:00')")
    attendees: List[str] = Field(default_factory=list, description="List of attendee email addresses")


class CreateCalendarEventTool(BaseTool):
    name: str = "Create Google Calendar Event Tool"
    description: str = "Creates a new event in Google Calendar."
    args_schema: Type[BaseModel] = CreateCalendarEventToolSchema

    def _run(self, summary: str, start_datetime_str: str, end_datetime_str: str, attendees: List[str] = None) -> str:
        """Creates a Google Calendar event."""
        attendees = attendees or []
        try:
            service = _get_calendar_service()
            event = {
                'summary': summary,
                'start': {'dateTime': start_datetime_str, 'timeZone': 'Asia/Kolkata'},
                'end': {'dateTime': end_datetime_str, 'timeZone': 'Asia/Kolkata'},
                'attendees': [{'email': e} for e in attendees],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }

            created = service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
            return f"Event created successfully: {created.get('htmlLink')}"

        except HttpError as e:
            return f"Google API error: {e}"
        except Exception as e:
            return f"Failed to create event: {e}"
