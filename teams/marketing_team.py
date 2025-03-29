from textwrap import dedent

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.python import PythonTools
from agno.storage.agent.sqlite import SqliteAgentStorage

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

# Define marketing team
marketing_team = UICompatibleTeam(
    name="Marketing Team",
    team_id="marketing_team",
    agent_id="marketing_team",
    description="End-to-end pipeline to generate personalized Crowe.com-based insights for board members.",
    model=OpenAIChat("gpt-4o"),
    members=[
        create_board_agent(),
        create_bod_interests_agent(),
        create_content_generator_agent(),
    ],
    mode="coordinate",
    enable_agentic_context=True,
    show_tool_calls=True,
    show_members_responses=True,
    markdown=True,
    instructions=[
        "You will receive the name of a company (e.g., 'PepsiCo').",
        "Use the Board Agent to find board members.",
        "For each member, identify their interests with the Interest Agent.",
        "Generate a personalized insights webpage with the Content Generator Agent.",
        "Confirm when all steps are complete and the content has been saved.",
    ],
    success_criteria="All board members have personalized pages created and listed in the index.",
    storage=SqliteAgentStorage(
        table_name="marketing_team",
        db_file="tmp/agents.db",
        mode="team"
    )
)
