from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage

# Custom tools
from tools.sec_api_tool import get_board_of_directors
from tools.save_html_tool import save_html_tool

# SQLite path (shared DB with other agents)
agent_storage = "tmp/agents.db"
PUBLIC_HTML_BASE_URL = "http://172.178.45.177:8080"

def create_marketing_agent() -> Agent:
    return Agent(
        name="Marketing Coordinator",
        agent_id="marketing_team",  # required for showing in Agent UI
        role="Coordinate personalized insights page generation for board members.",
        model=OpenAIChat("gpt-4o"),
        tools=[
            get_board_of_directors,
            save_html_tool,
        ],
        instructions=dedent(f"""
            You are coordinating the generation of personalized web pages for the board of directors of a company.

            1. Receive the company name (e.g., 'PepsiCo')
            2. Use the SEC API tool to fetch board members.
            3. For each member, identify their interests and generate a personalized HTML page.
            4. Save the webpage using SaveHTMLTool and update the index.
            5. Provide a confirmation message and public URLs: {PUBLIC_HTML_BASE_URL}/<filename>.html
        """),
        markdown=True,
        show_tool_calls=True,
        add_history_to_messages=True,
        add_datetime_to_instructions=True,
        num_history_responses=5,
        storage=SqliteAgentStorage(
            table_name="marketing_team",
            db_file=agent_storage
        )
    )
