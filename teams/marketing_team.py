import asyncio
from pathlib import Path
from textwrap import dedent

from agno.models.openai import OpenAIChat
from agno.agent import Agent
from agno.team.team import Team
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.python import PythonTools
from tools.sec_api_tool import get_board_of_directors
from tools.save_html_tool import save_html_tool

# Load our existing agents
from agents.mkt_bod_interests import create_bod_interests_agent
from agents.mkt_content_generator import create_content_generator_agent

# Use the public folder for storing the pages
PUBLIC_HTML_BASE_URL = "http://172.178.45.177:8080"

# Wrappers to dynamically call the loaded agents
bod_interest_agent = create_bod_interests_agent()
content_generator_agent = create_content_generator_agent()

# Primary controller agent
coordinator_agent = Agent(
    name="Marketing Coordinator",
    role="Coordinate marketing website generation for board members.",
    model=OpenAIChat("gpt-4o"),
    tools=[get_board_of_directors, save_html_tool],
    add_name_to_instructions=True,
    instructions=dedent(f"""
        You are coordinating the generation of personalized web pages for the board of directors of a company.
        1. Receive a company name (e.g., 'PepsiCo')
        2. Use the SEC tool to retrieve board members
        3. For each member, call the mkt_bod_interests agent to extract interests
        4. Then call the mkt_content_generator agent with their name and interests
        5. Use the SaveHTMLTool to write each HTML to public folder
        6. Confirm completion and list links to the generated pages using the base URL: {PUBLIC_HTML_BASE_URL}
    """),
    show_tool_calls=True,
    markdown=True,
)

# Create the team to orchestrate the flow
marketing_team = Team(
    name="Board Content Team",
    mode="collaborate",
    model=OpenAIChat("gpt-4o"),
    members=[
        coordinator_agent,
        bod_interest_agent,
        content_generator_agent
    ],
    instructions=[
        "You are working together to generate a personalized webpage for each board member of a given company.",
        "The coordinator agent is in charge of leading the process step by step."
    ],
    success_criteria="All pages are successfully generated and saved to the server.",
    enable_agentic_context=True,
    show_tool_calls=True,
    show_members_responses=True,
    markdown=True,
)

if __name__ == "__main__":
    asyncio.run(
        marketing_team.aprint_response(
            message="Generate personalized insights webpages for PepsiCo board members.",
            stream=True,
            stream_intermediate_steps=True,
        )
    )
