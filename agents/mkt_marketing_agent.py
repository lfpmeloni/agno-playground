from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage

# Custom tools
from tools.sec_api_tool import get_board_of_directors
from tools.save_html_tool import save_html_tool

# Other agents as tools
from agents.mkt_board_of_directors import create_board_agent
from agents.mkt_bod_interests import create_bod_interests_agent
from agents.mkt_content_generator import create_content_generator_agent

agent_storage = "tmp/agents.db"
PUBLIC_HTML_BASE_URL = "http://172.178.45.177:8080"

marketing_team = Agent(
    name="Marketing Coordinator",
    agent_id="marketing_team",  # Required for Agent UI
    role="Coordinate the generation of personalized webpages for board members of public companies.",
    model=OpenAIChat("gpt-4o"),
    tools=[
        get_board_of_directors,
        save_html_tool,
    ],
    instructions=dedent(f"""
        You are coordinating the generation of personalized web pages for the board of directors of a company.

        1. Receive the company name (e.g., 'PepsiCo')
        2. Use the SEC API tool to fetch board members.
        3. For each member, ask the 'Interest Agent' for their interests.
        4. Then ask the 'Content Generator Agent' to create a webpage based on their interests.
        5. Use the SaveHTMLTool to save the webpage and update the index.
        6. Provide a confirmation message and links to all generated pages at: {PUBLIC_HTML_BASE_URL}
        
        Available agents for internal delegation:
        - Interest Agent: mkt_bod_interests
        - Content Generator Agent: mkt_content_generator
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
