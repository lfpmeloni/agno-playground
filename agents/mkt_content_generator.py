from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools.duckduckgo import DuckDuckGoTools
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
            PythonTools(),
            save_html_tool
        ],
        instructions=[
            "You will receive the name of a board member and a list of interests.",
            "Perform **no more than 3 total DuckDuckGo queries**. Combine keywords efficiently, e.g., 'site:Crowe.com governance AND leadership'.",
            "Focus only on Crowe.com results. If none are found, mention that gracefully.",
            "Extract key insights from those articles and reframe them in a way that matches the board member’s background or interest area.",
            "Build a clean, standalone HTML page. Save it using the SaveHTMLTool, following the format 'first-last.html'.",
            "DO NOT print or echo the HTML in your response — only confirm the save.",
            "Respond only with a short success message and the correct public link: http://172.178.45.177:8080/<filename>",
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