"""
main.py
-------
Main entry point for Multi-Agent Personal Workflow Assistant.
"""

import os
import sys
import traceback
from datetime import datetime
from dotenv import load_dotenv
from crewai import Crew, Process

# Add current directory to Python path
sys.path.insert(0, os.getcwd())

# Load environment variables FIRST
load_dotenv()

# Import AFTER environment loading
try:
    from agents import WorkflowAgents
    from tasks import WorkflowTasks
    print("✅ All modules imported successfully")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("💡 Check: agents.py, tasks.py, productivity_tools.py exist?")
    input("Press Enter to exit...")
    sys.exit(1)

def validate_environment():
    """Check required setup"""
    missing = []
    
    # Check OpenAI (optional - mock tools work without it)
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  No OPENAI_API_KEY - using fallback LLM (OK for testing)")
    
    # Check files
    required_files = ["agents.py", "tasks.py", "productivity_tools.py"]
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print(f"❌ Missing files: {', '.join(missing)}")
        return False
    
    print("✅ Environment validated")
    return True

def main():
    """
    Main workflow execution.
    """
    print("==================================================")
    print("🤖 Multi-Agent Personal Workflow Assistant 🤖")
    print("==================================================")
    
    # Validate setup
    if not validate_environment():
        input("\nPress Enter to exit...")
        return
    
    print("\nWhat can I help you with today?")
    user_request = input("> ").strip()
    
    if not user_request:
        print("❌ No request provided.")
        return
    
    print("\n==================================================")
    print("🚀 Crew is assembled. Kicking off workflow...")
    print("==================================================")
    
    try:
        # Initialize classes
        agents_class = WorkflowAgents()
        tasks_class = WorkflowTasks()
        
        print("🧪 Creating agents...")
        # Create agent instances
        info_fetcher_agent = agents_class.info_fetcher_agent()
        analyzer_agent = agents_class.analyzer_agent()
        executor_agent = agents_class.executor_agent()
        
        print("📋 Creating tasks...")
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
        
        print("👥 Forming crew...")
        crew = Crew(
            agents=[info_fetcher_agent, analyzer_agent, executor_agent],
            tasks=[fetch_info_task, analyze_data_task, execute_tasks_task],
            process=Process.sequential,
            verbose=True,
            memory=False,
            max_rpm=10,
            share_crew=False
        )
        
        print("🚀 Executing workflow...")
        result = crew.kickoff()
        
        print("\n" + "="*60)
        print("🎉 WORKFLOW COMPLETE! 🎉")
        print("="*60)
        print(f"✅ Final Result:\n{result}")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Workflow failed: {str(e)}")
        print(f"\n🔍 Full traceback:")
        traceback.print_exc()
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()