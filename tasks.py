"""
tasks.py
--------
Defines the tasks for the workflow.
"""

from crewai import Task
from datetime import datetime, timedelta


class WorkflowTasks:
    """
    Defines the tasks for the workflow agents.
    """
    
    def fetch_info_task(self, agent, user_request) -> Task:
        """Task 1: Search and scrape SpaceX launch info"""
        return Task(
            description=f"Use the DuckDuckGoSearchTool to find the latest SpaceX launch announcements. The search query is: 'latest SpaceX launch key announcements site:spacex.com OR site:nasa.gov'. "
                        f"Then, use the ScrapeWebsiteTool to scrape the content of the top 2-3 search results. Combine the scraped content into a single block of text. "
                        f"The user's request was: {user_request}",
            expected_output="A single block of text containing the raw content from the scraped websites, and a list of the URLs that were scraped.",
            agent=agent
        )

    def analyze_data_task(self, agent, user_request, context) -> Task:
        """Task 2: Analyze data and create JSON action plan"""
        tomorrow = datetime.now() + timedelta(days=1)
        start_time = tomorrow.strftime("%Y-%m-%dT16:00:00")
        end_time = tomorrow.strftime("%Y-%m-%dT16:30:00")

        return Task(
            description=f"Analyze the provided text to identify the key announcements from the SpaceX launch. Based on the analysis, create a 1-paragraph summary. "
                        f"Then, create a JSON object with two keys: 'email_action' and 'calendar_action'. Make sure to use the recipient's email address for both the email and the calendar event. "
                        f"The start time for the calendar event is {start_time} and the end time is {end_time}. The user's request was: {user_request}",
            expected_output="A JSON object with the keys 'email_action' and 'calendar_action', containing the summary and the meeting details.",
            agent=agent,
            context=context
        )

    def execute_tasks_task(self, agent, context) -> Task:
        """Task 3: Execute email and calendar actions"""
        return Task(
            description="Execute the actions from the JSON plan. You must use the SendEmailTool to send the email and the CreateCalendarEventTool to create the calendar event. Do not simulate the results. Report the exact output from each tool.",
            expected_output="A report confirming the successful execution of the email and calendar actions, with the exact output from each tool.",
            agent=agent,
            context=context
        )