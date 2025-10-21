# Multi-Agent Personal Workflow Assistant

This project is a multi-agent personal workflow assistant built with the `crewai` framework. It can automate tasks like searching the internet, analyzing information, and performing actions such as sending emails and creating calendar events. The project includes both a command-line interface (CLI) and a web-based interface built with Streamlit.

## Features

*   **Multi-Agent System:** Utilizes the `crewai` framework to create a team of AI agents that collaborate to complete tasks.
*   **Information Retrieval:** Searches the internet for up-to-date information using DuckDuckGo.
*   **Web Scraping:** Scrapes websites to extract relevant content.
*   **Data Analysis:** Analyzes the gathered information to generate summaries and action plans.
*   **Email Automation:** Sends emails using your Gmail account.
*   **Calendar Integration:** Creates events in your Google Calendar.
*   **Dual Interfaces:** Can be run as a command-line application or as a web-based application using Streamlit.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.8+
*   pip

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/15sam/crewai-personal-assistant.git
    cd crewai-personal-assistant
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1.  **Environment Variables:**
    *   Rename the `.env.example` file to `.env`.
    *   Open the `.env` file and fill in the following values:
        *   `OPENAI_API_KEY`: Your API key for the OpenAI language model.
        *   `EMAIL_SENDER`: Your Gmail address for sending emails.
        *   `EMAIL_PASSWORD`: Your Gmail app password.

2.  **Google Calendar API:**
    *   Follow the instructions in the [Google Calendar API Python Quickstart](https://developers.google.com/calendar/api/quickstart/python) to enable the API and download your `credentials.json` file.
    *   Place the `credentials.json` file in the root directory of the project.
    *   The first time you run the application, you will be prompted to authorize access to your Google Calendar.

### Running the Application

You can run the assistant in two ways:

1.  **Command-Line Interface (CLI):**
    ```bash
    python main.py
    ```

2.  **Web-Based Interface (Streamlit):**
    ```bash
    streamlit run app.py
    ```

## Project Structure

*   `main.py`: The entry point for the command-line interface.
*   `app.py`: The entry point for the Streamlit web interface.
*   `agents.py`: Defines the agents that make up the crew (e.g., information fetcher, analyzer, executor).
*   `tasks.py`: Defines the tasks that the agents will perform.
*   `productivity_tools.py`: Contains the custom tools used by the agents (e.g., search, scrape, send email, create calendar event).
*   `requirements.txt`: A list of the Python packages required to run the project.
*   `.env.example`: A template for the environment variables file.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
