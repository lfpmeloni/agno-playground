from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools import tool
import os

HR_DOCS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../hr_docs"))

@tool
def read_client_work() -> str:
    """Read the CLIENT_WORK.txt file."""
    path = os.path.join(HR_DOCS_FOLDER, "CLIENT_WORK.txt")
    if not os.path.exists(path):
        return "No client work file found."
    with open(path, "r") as f:
        return f.read()

def create_client_work_agent():
    return Agent(
        name="HR Client Work Agent",
        agent_id="hr_client_work_agent",
        role="Analyzes the employee's client work for quarterly review.",
        model=OpenAIChat("gpt-4o"),
        tools=[read_client_work],
        instructions="""
            You are an HR specialist evaluating the employee's client work.
            Use the `read_client_work` tool to access the document.
            Identify key achievements, contributions to clients, and any standout initiatives.
            Present your findings as a short summary of client impact and work quality.
        """,
        markdown=True,
        show_tool_calls=True,
        add_datetime_to_instructions=True,
        storage=SqliteAgentStorage(table_name="hr_client_work", db_file="tmp/agents.db")
    )
