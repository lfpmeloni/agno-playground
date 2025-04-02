from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools import tool
import os

HR_DOCS_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), "../hr_docs"))

@tool
def read_feedback() -> str:
    """Read the FEEDBACK.txt file."""
    path = os.path.join(HR_DOCS_FOLDER, "FEEDBACK.txt")
    if not os.path.exists(path):
        return "No feedback file found."
    with open(path, "r") as f:
        return f.read()

def create_feedback_agent():
    return Agent(
        name="HR Feedback Agent",
        agent_id="hr_feedback_agent",
        role="Analyzes employee feedback for quarterly review.",
        model=OpenAIChat("gpt-4o"),
        tools=[read_feedback],
        instructions="""
            You are an HR specialist responsible for summarizing the employee feedback.
            Use the `read_feedback` tool to retrieve the feedback content.
            Then analyze it to highlight the employee's strengths, recurring themes, and concerns raised by peers.
            Summarize your findings in a few bullet points.
        """,
        markdown=True,
        show_tool_calls=True,
        add_datetime_to_instructions=True,
        storage=SqliteAgentStorage(table_name="hr_feedback", db_file="tmp/agents.db")
    )
