import asyncio
import json
from textwrap import dedent
from agno.models.openai import OpenAIChat
from agno.team.team import Team
from agno.storage.agent.sqlite import SqliteAgentStorage

# Custom agents used as team members
from agents.mkt_board_of_directors import create_board_agent
from agents.mkt_bod_interests import create_bod_interests_agent
from agents.mkt_content_generator import create_content_generator_agent

# DuckDuckGo pre-search
from duckduckgo_search import DDGS

# Storage and base URL
agent_storage = "tmp/agents.db"
PUBLIC_HTML_BASE_URL = "http://172.178.45.177:8080"

# Pre-search using DDG (before agents run)
def run_duckduckgo_once(board_member_name):
    query = f"{board_member_name} PepsiCo leadership site:Crowe.com"
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(keywords=query, max_results=5))
            return json.dumps(results, indent=2)
    except Exception as e:
        print("[WARNING] DuckDuckGo pre-search failed:", e)
        return "[]"

async def main():
    # Step 1: get the board
    board_agent = create_board_agent()
    board_response = await board_agent.arun("Get the board of directors for PepsiCo using the SEC API")
    board_list = board_response.get("result", []) if isinstance(board_response, dict) else []

    if not board_list:
        print("❌ Failed to fetch board of directors.")
        return

    # Step 2: focus on the last board member
    last_member = board_list[-1] if isinstance(board_list[-1], dict) else {"name": board_list[-1].split(" - ")[0], "title": board_list[-1].split(" - ")[1] if ' - ' in board_list[-1] else ""}
    last_name = last_member.get("name")
    last_title = last_member.get("title")

    # Step 3: run DDG once and inject result into context
    ddg_results = run_duckduckgo_once(last_name)

    # Define the full team
    marketing_team = Team(
        name="Marketing Team",
        team_id="marketing_team",
        description="Fetch board members, extract interests, generate Crowe.com-style pages.",
        model=OpenAIChat("gpt-4o"),
        mode="coordinate",
        members=[
            board_agent,
            create_bod_interests_agent(),
            create_content_generator_agent(),
        ],
        instructions=[
            "You are the coordinator of a marketing automation pipeline.",
            "The goal is to generate a Crowe.com-style insights page for the last board member.",
            "You already have the board list, and DDG results for the last member are provided.",
            "Step 1: Use the provided board list to identify the last member.",
            "Step 2: Call the Interest Agent to extract inferred interests using ONLY the context or provided DDG URLs.",
            "Step 3: Call the Content Generator Agent with the name and inferred interests.",
            f"Ensure the page is saved using SaveHTMLTool and accessible at {PUBLIC_HTML_BASE_URL}/<filename>.html.",
            "Return a final summary with the board member name and the link to the generated page."
        ],
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

    await marketing_team.aprint_response(
        message=f"Generate insights page for {last_name}, {last_title} at PepsiCo.",
        context={
            "board_members": board_list,
            "last_board_member": last_member,
            "ddg_results": ddg_results
        },
        stream=True,
        stream_intermediate_steps=True
    )

if __name__ == "__main__":
    asyncio.run(main())
