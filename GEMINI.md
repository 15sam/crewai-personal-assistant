# GEMINI.md

## Project Overview

This project is a multi-agent personal workflow assistant built with the `crewai` framework in Python. It automates tasks by defining a series of agents that collaborate to achieve a goal.

The core components are:

*   **`main.py`**: The entry point of the application. It initializes the agents, tasks, and the crew, and then kicks off the workflow.
*   **`agents.py`**: Defines the three agents in the crew:
    *   `info_fetcher_agent`: Searches the internet and scrapes websites for information.
    *   `analyzer_agent`: Analyzes the gathered information and creates a JSON plan for the next steps.
    *   `executor_agent`: Executes the plan, which can involve sending emails and creating calendar events.
*   **`tasks.py`**: Defines the tasks that each agent will perform.
*   **`productivity_tools.py` and `tools/`**: These files contain the custom tools used by the agents, such as:
    *   `SearchInternetTool`: For searching the web.
    *   `ScrapeWebsiteTool`: For scraping web pages.
    *   `SendEmailTool`: For sending emails.
    *   `CreateCalendarEventTool`: For creating Google Calendar events.
*   **`.env.example`**: A template for the required environment variables.

## Building and Running

To run this project, follow these steps:

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Environment:**
    *   Rename `.env.example` to `.env`.
    *   Fill in the required API keys and credentials in the `.env` file:
        *   `OPENAI_API_KEY`: For the language model.
        *   `GOOGLE_API_KEY`: For Google Custom Search.
        *   `GOOGLE_CSE_ID`: Your Custom Search Engine ID.
        *   `EMAIL_SENDER`: Your Gmail address.
        *   `EMAIL_PASSWORD`: Your Gmail app password.
    *   You will also need a `credentials.json` file for the Google Calendar API.

3.  **Run the Application:**
    ```bash
    python main.py
    ```
    The application will then prompt you for a request.

## Development Conventions

*   The project follows a modular structure, separating agents, tasks, and tools into different files.
*   The agents are designed to be specialized for their roles.
*   The tasks are chained together, with the output of one task feeding into the next.
*   The use of a `.env` file keeps sensitive information separate from the code.
