import asyncio
import os
from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.storage.agent.sqlite import SqliteAgentStorage

from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.python import PythonTools

# Custom tools
from tools.sec_api_tool import get_board_of_directors
from tools.save_html_tool import save_html_tool

# Custom agents
from agents.mkt_board_of_directors import create_board_agent
from agents.mkt_bod_interests import create_bod_interests_agent
from agents.mkt_content_generator import create_content_generator_agent

# Base URL to access public HTML pages
PUBLIC_HTML_BASE_URL = "http://172.178.45.177:8080"

class UICompatibleTeam(Team):
    @property
    def agent_id(self):
        return self.team_id

# Coordinator (optional for orchestration)
coordinator_agent = Agent(
    name="Marketing Coordinator",
    role="Coordinate the generation of personalized webpages for board members.",
    model=OpenAIChat("gpt-4o"),
    tools=[get_board_of_directors, save_html_tool],
    instructions=dedent(f"""
        You are coordinating the generation of personalized web pages for the board of directors of a company.
        1. Receive a company name (e.g., 'PepsiCo')
        2. Use the SEC API tool to fetch board members
        3. For each member, call the Interest Agent to identify their interests
        4. Then call the Content Generator Agent to create a personalized HTML page
        5. Use the SaveHTMLTool to write the HTML file and update the index
        6. Return confirmation and public links using: {PUBLIC_HTML_BASE_URL}/<name>.html
    """),
    show_tool_calls=True,
    markdown=True,
)

# Team to orchestrate the full pipeline
marketing_team = UICompatibleTeam(
    name="Marketing Team",
    team_id="marketing_team",  # This will now also serve as agent_id
    description="End-to-end workflow to generate personalized Crowe.com-based pages for board members.",
    model=OpenAIChat(id="gpt-4o"),
    members=[
        create_board_agent(),
        create_bod_interests_agent(),
        create_content_generator_agent(),
    ],
    mode="coordinate",
    instructions=[
        "You will receive the name of a company (e.g., 'PepsiCo').",
        "Use the Board Agent to find board members.",
        "For each member, identify their interests with the Interest Agent.",
        "Generate a personalized insights webpage with the Content Generator Agent.",
        "Confirm when all steps are complete and the content has been saved.",
    ],
    success_criteria="All board members have personalized pages created and listed in the index.",
    show_tool_calls=True,
    show_members_responses=True,
    markdown=True,
    enable_agentic_context=True,
    storage=SqliteAgentStorage(
        table_name="marketing_team",
        db_file="tmp/agents.db",
        mode="team"
    )
)

# Run manually (for debugging, optional)
if __name__ == "__main__":
    asyncio.run(
        marketing_team.aprint_response(
            message="Generate personalized insights webpages for PepsiCo board members.",
            stream=True,
            stream_intermediate_steps=True,
        )
    )
