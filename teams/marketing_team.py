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
    team_id="marketing_team",  # used for logs and reuse
    description="End-to-end pipeline: fetch board members, extract interests, and generate personalized pages.",
    model=OpenAIChat("gpt-4o"),
    mode="coordinate",  # Team leader delegates work and aggregates output
    members=[
        create_board_agent(),
        create_bod_interests_agent(),
        create_content_generator_agent(),
    ],
    instructions=[
        "You are the leader of a marketing automation team tasked with generating Crowe.com-style insights pages for board members.",
        "You will receive a company name (e.g., 'PepsiCo').",
        "Step 1: Call the Board Agent to fetch the board of directors using the SEC API.",
        "Step 2: Focus ONLY on the LAST board member returned. Pass their name and title to the Interest Agent.",
        "Step 3: The Interest Agent must identify the person’s likely professional interests.",
        "⚠️ Limit DuckDuckGo usage to a SINGLE query per agent per person. Combine all inferred interest areas into one query.",
        "⚠️ If DuckDuckGo fails or is unavailable, fallback to inferring interests from the person’s title and background.",
        "Step 4: Call the Content Generator Agent with a SINGLE combined search term string (e.g., 'healthcare finance governance').",
        f"Use only one DuckDuckGo search with the format: site:Crowe.com <combined-interests>",
        f"Ensure that each page is saved using SaveHTMLTool and made accessible via: {PUBLIC_HTML_BASE_URL}/<filename>.html",
        "Return a final summary listing the board member's name and the public URL of the generated page.",
    ],
    success_criteria=(
        "The insights page for the last board member is created, saved, and publicly accessible. "
        "Summary includes the final link."
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
