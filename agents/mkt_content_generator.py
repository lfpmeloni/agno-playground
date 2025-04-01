from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.python import PythonTools

from tools.save_html_tool import save_html_tool
import os

# Directory where the generated HTML files will be saved
PUBLIC_HTML_DIR = os.path.join(os.path.dirname(__file__), "../public")
os.makedirs(PUBLIC_HTML_DIR, exist_ok=True)

def create_content_generator_agent():
    return Agent(
        name="mkt_content_generator",
        description=(
            "Generates personalized HTML content using Crowe.com articles based on the interests of a board member."
        ),
        model=OpenAIChat(id="gpt-4o"),
        tools=[
            DuckDuckGoTools(),
            GoogleSearchTools(),
            PythonTools(),
            save_html_tool
        ],
        instructions=[
            "You will receive the name of a board member and a list of their verified or inferred interests.",
            "Search Crowe.com using 1 combined query like: site:Crowe.com <interest 1> AND <interest 2>.",
            "If DuckDuckGo fails, use GoogleSearchTools to find matching pages from Crowe.com.",
            "Read and summarize key insights from the articles retrieved. Tailor them to reflect the board member’s leadership style, priorities, and strategic interests.",
            "Organize the insights in three sections: Personal Interests, Recent Activities, and Business Insights — these must be filled with meaningful, personalized content.",
            "Create a clean standalone HTML file and save it using SaveHTMLTool, following the 'first-last.html' format.",
            "DO NOT print or display the HTML. Only return a confirmation and the link: http://172.178.45.177:8080/<filename>.html."
        ],
        markdown=True,
        show_tool_calls=True,
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        storage=SqliteAgentStorage(
            table_name="content_generator",
            db_file="tmp/agents.db"
        )
    )