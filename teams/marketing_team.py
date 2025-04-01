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
    team_id="marketing_team",  # used for logs and reuse, not for Agent UI yet
    description="End-to-end pipeline: fetch board members, extract interests, and generate personalized pages.",
    model=OpenAIChat("gpt-4o"),
    mode="coordinate",  # Team leader delegates work and aggregates output
    members=[
        create_board_agent(),
        create_bod_interests_agent(),
        create_content_generator_agent(),
    ],
    instructions=[
        "You are the leader of a marketing automation team.",
        "You will receive a company name (e.g., 'PepsiCo').",
        "First, use the Board Agent to fetch the board of directors.",
        "For ONLY THE LAST board member, call the Interest Agent to determine key interests.",
        "Avoid using Wikipedia unless absolutely necessary. Use DuckDuckGo sparingly—at most 1 query per member per agent.",
        "If DuckDuckGo fails or rate limits, fallback to general inference from the board member name and title.",
        "Then, call the Content Generator Agent to create a Crowe.com-style personalized insights page.",
        f"Ensure the pages are saved using the SaveHTMLTool and indexed at: {PUBLIC_HTML_BASE_URL}/<name>.html",
        "Finish with a summary and confirmation message.",
    ],
    success_criteria="All board members have personalized pages created and saved. A summary is returned with all links.",
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
