from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools import tool
import os

HR_DOCS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../hr_docs"))

@tool
def read_bold_goals() -> str:
    """Read the BOLD_GOALS.txt file."""
    path = os.path.join(HR_DOCS_FOLDER, "BOLD_GOALS.txt")
    if not os.path.exists(path):
        return "No BOLD_GOALS file found."
    with open(path, "r") as f:
        return f.read()

def create_goal_alignment_agent():
    return Agent(
        name="HR Goal Alignment Agent",
        agent_id="hr_goal_alignment_agent",
        role="Assesses how the employee’s work and feedback align with yearly goals.",
        model=OpenAIChat("gpt-4o"),
        tools=[read_bold_goals],
        instructions="""
            You are responsible for evaluating whether the employee's work aligns with their BOLD_GOALS.
            Use the `read_bold_goals` tool to retrieve the goals.
            Summarize the primary objectives and evaluate how well the feedback and client work support them.
            Highlight key achievements, gaps, and any outstanding goals.
        """,
        markdown=True,
        show_tool_calls=True,
        add_datetime_to_instructions=True,
        storage=SqliteAgentStorage(table_name="hr_goal_alignment", db_file="tmp/agents.db")
    )
