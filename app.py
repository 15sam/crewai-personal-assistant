import streamlit as st
import os
import sys
from dotenv import load_dotenv
from crewai import Crew, Process

# Add current directory to Python path
sys.path.insert(0, os.getcwd())

# Load environment variables
load_dotenv()

# Import AFTER environment loading
try:
    from agents import WorkflowAgents
    from tasks import WorkflowTasks
except ImportError as e:
    st.error(f"Import failed: {e}")
    st.stop()

def run_workflow(user_request):
    """
    Runs the CrewAI workflow based on the user's request.
    """
    try:
        # Initialize classes
        agents_class = WorkflowAgents()
        tasks_class = WorkflowTasks()

        # Create agent instances
        info_fetcher_agent = agents_class.info_fetcher_agent()
        analyzer_agent = agents_class.analyzer_agent()
        executor_agent = agents_class.executor_agent()

        # Create task chain
        fetch_info_task = tasks_class.fetch_info_task(info_fetcher_agent, user_request)
        analyze_data_task = tasks_class.analyze_data_task(
            agent=analyzer_agent,
            user_request=user_request,
            context=[fetch_info_task]
        )
        execute_tasks_task = tasks_class.execute_tasks_task(
            agent=executor_agent,
            context=[analyze_data_task]
        )

        # Form the crew
        crew = Crew(
            agents=[info_fetcher_agent, analyzer_agent, executor_agent],
            tasks=[fetch_info_task, analyze_data_task, execute_tasks_task],
            process=Process.sequential,
            verbose=True,
            memory=False,
            max_rpm=10,
            share_crew=False
        )

        # Execute the workflow
        result = crew.kickoff()
        return result

    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit UI
st.title("Multi-Agent Personal Workflow Assistant")

user_request = st.text_input("What can I help you with today?")

if st.button("Start Workflow"):
    if user_request:
        with st.spinner("The crew is on the job..."):
            result = run_workflow(user_request)
            st.success("Workflow Complete!")
            if isinstance(result, str):
                st.write(result)
            else:
                st.write(result.raw)
    else:
        st.warning("Please enter a request.")
