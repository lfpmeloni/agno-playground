from textwrap import dedent
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools import tool
import os

HR_DOCS_FOLDER = "playground/hr_docs"
AGENT_DB_PATH = "tmp/agents.db"

# Custom tool that loads and formats the review documents
@tool
def read_hr_documents() -> str:
    """Loads all HR documents: FEEDBACK.txt, CLIENT_WORK.txt, and BOLD_GOALS.txt from the hr_docs folder."""
    def safe_read(file_name):
        path = os.path.join(HR_DOCS_FOLDER, file_name)
        if not os.path.isfile(path):
            return f"{file_name} not found.\n"
        with open(path, "r") as f:
            return f.read()

    feedback = safe_read("FEEDBACK.txt")
    client_work = safe_read("CLIENT_WORK.txt")
    bold_goals = safe_read("BOLD_GOALS.txt")

    return f"""
--- FEEDBACK ---
{feedback}

--- CLIENT WORK ---
{client_work}

--- BOLD GOALS ---
{bold_goals}
"""

# Create the agent
def create_quarterly_review_agent():
    return Agent(
        name="Quarterly Review Agent",
        agent_id="hr_quarterly_review",
        role="HR assistant that reviews quarterly performance based on feedback, client work, and yearly goals.",
        model=OpenAIChat("gpt-4o"),
        tools=[read_hr_documents],
        instructions=dedent("""
            You are an HR assistant helping with quarterly performance reviews.
            Use the `read_hr_documents` tool to retrieve all necessary context.
            Then analyze and summarize how the feedback and client work align with the BOLD_GOALS.
            Your summary should:
            - Mention strengths and progress
            - Highlight gaps or areas for improvement
            - Reference specific quotes or examples
        """),
        markdown=True,
        show_tool_calls=True,
        add_history_to_messages=False,
        add_datetime_to_instructions=True,
        storage=SqliteAgentStorage(
            table_name="hr_quarterly_review",
            db_file=AGENT_DB_PATH
        )
    )