from textwrap import dedent
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.storage.agent.sqlite import SqliteAgentStorage

# Custom agents used as team members
from agents.mkt_board_of_directors import create_board_agent
from agents.mkt_bod_interests import create_bod_interests_agent
from agents.mkt_content_generator import create_content_generator_agent

# Storage and base URL
agent_storage = "tmp/agents.db"
PUBLIC_HTML_BASE_URL = "http://172.178.45.177:8080"

# Define the full team as a coordinator
marketing_team = Team(
    name="Marketing Team",
    team_id="marketing_team",
    description="End-to-end pipeline: fetch board members, extract interests, and generate personalized pages.",
    model=OpenAIChat("gpt-4o"),
    mode="coordinate",
    members=[
        create_board_agent(),
        create_bod_interests_agent(),
        create_content_generator_agent(),
    ],
    instructions=[
        "You are the leader of a marketing automation team tasked with generating Crowe.com-style insights pages for board members.",
        "You will receive a company name (e.g., 'PepsiCo').",
        "Your job is to coordinate the team to retrieve the board of directors, identify interests, and generate a personalized insights page for one board member.",
        "Use only 1 search query per agent. If search tools fail, fallback to inferring based on titles and roles.",
        f"All final pages must be saved using SaveHTMLTool and served at: {PUBLIC_HTML_BASE_URL}/<filename>.html",
        "The page must contain real, personalized content derived from web search. Do not return placeholder templates."
        "The final response should include the board member's name and the public link to their page.",
    ],
    success_criteria=(
        "A personalized HTML insights page is created and publicly accessible. The board member's name and the link are returned."
    ),
    enable_agentic_context=True,
    show_tool_calls=True,
    show_members_responses=True,
    markdown=True,
    storage=SqliteAgentStorage(
        table_name="marketing_team",
        db_file=agent_storage,
        mode="team"
    )
)

if __name__ == "__main__":
    import asyncio
    asyncio.run(
        marketing_team.aprint_response(
            message="Generate personalized insights webpages for PepsiCo board members.",
            stream=True,
            stream_intermediate_steps=True,
        )
    )
