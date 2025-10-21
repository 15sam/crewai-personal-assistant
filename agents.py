"""
agents.py
---------
Defines the agents for the workflow.
"""

import os
from crewai import Agent
from langchain_openai import ChatOpenAI
from dotenv import dotenv_values

from productivity_tools import (
    DuckDuckGoSearchTool, 
    ScrapeWebsiteTool, 
    SendEmailTool, 
    CreateCalendarEventTool
)

class WorkflowAgents:
    """
    Agents using the OpenAI language model.
    """
    def __init__(self):
        config = dotenv_values(".env")
        api_key = config.get("OPENAI_API_KEY")
        self.llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=api_key)

    def info_fetcher_agent(self):
        return Agent(
            role="Information Retrieval Specialist",
            goal="Use tools to find SpaceX launch information.",
            backstory="You use DuckDuckGoSearchTool and ScrapeWebsiteTool to gather data.",
            tools=[DuckDuckGoSearchTool(), ScrapeWebsiteTool()],
            llm=self.llm,
            verbose=True,
            max_iter=2,
            allow_delegation=True
        )

    def analyzer_agent(self):
        return Agent(
            role="Data Analyst and Planner",
            goal="Create JSON action plan from scraped data.",
            backstory="You analyze data and output valid JSON for email/calendar actions.",
            llm=self.llm,
            verbose=True,
            max_iter=1
        )

    def executor_agent(self):
        return Agent(
            role="Task Executor and Coordinator",
            goal="Execute JSON plan using email and calendar tools.",
            backstory="You use SendEmailTool and CreateCalendarEventTool to perform actions.",
            tools=[SendEmailTool(), CreateCalendarEventTool()],
            llm=self.llm,
            verbose=True,
            max_iter=2,
            allow_delegation=True
        )