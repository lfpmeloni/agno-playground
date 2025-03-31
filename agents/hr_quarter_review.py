from textwrap import dedent
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage

# Paths
HR_DOCS_FOLDER = "playground/hr_docs"
AGENT_DB_PATH = "tmp/agents.db"

def create_quarterly_review_agent():
    return Agent(
        name="Quarterly Review Agent",
        agent_id="hr_quarterly_review",
        role="HR assistant reviewing employee performance based on feedback, client work, and yearly goals.",
        model=OpenAIChat("gpt-4o"),
        instructions=dedent("""
            You are an HR assistant that helps with quarterly employee performance reviews.
            Your role is to:
            1. Read the feedback received by the employee.
            2. Analyze the documented client work.
            3. Match both to the BOLD_GOALS of the employee.
            4. Summarize how the employee’s actions and received feedback align with their yearly goals.

            You'll be provided with three sections: FEEDBACK, CLIENT_WORK, and BOLD_GOALS. Review each and produce a structured summary that discusses:
            - Strengths and progress made towards goals.
            - Any noted gaps or opportunities for improvement.
            - Specific quotes or accomplishments aligned with goals.
        """),
        markdown=True,
        show_tool_calls=False,
        add_history_to_messages=False,
        add_datetime_to_instructions=True,
        storage=SqliteAgentStorage(
            table_name="hr_quarterly_review",
            db_file=AGENT_DB_PATH
        ),
        input_template=dedent("""
            --- FEEDBACK ---
            {feedback}

            --- CLIENT WORK ---
            {client_work}

            --- BOLD GOALS ---
            {bold_goals}
        """)
    )
