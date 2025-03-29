from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.python import PythonTools

from tools.save_html_tool import SaveHTMLTool
import os

# Directory where the generated HTML files will be saved
PUBLIC_HTML_DIR = os.path.join(os.path.dirname(__file__), "../public")
os.makedirs(PUBLIC_HTML_DIR, exist_ok=True)

def create_content_generator_agent():
    return Agent(
        name="mkt_content_generator",
        description=(
            "Generates personalized website content using articles from Crowe.com based on the interests of a board member."
        ),
        model=OpenAIChat(id="gpt-4o"),
        tools=[
            DuckDuckGoTools(),
            PythonTools(),
            SaveHTMLTool()
        ],
        instructions=[
            "You will be given the name of a board member and a list of their interests.",
            "Use DuckDuckGo to search for site:Crowe.com + each interest keyword to find relevant articles.",
            "Summarize or rephrase key insights from these articles and personalize them for the given individual.",
            "Structure the final output as a full standalone HTML page.",
            "Call the SaveHTMLTool with the filename (e.g., daniel-vasella.html) and HTML content to save it to the public/ directory.",
            "Also update or append the file 'public/index.html' with a link to the new personalized HTML page.",
            "Add titles, sections, source links, and a timestamp. Keep it professional and readable."
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
