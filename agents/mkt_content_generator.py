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
            "Generates personalized website content using articles from Crowe.com based on the interests of a board member."
        ),
        model=OpenAIChat(id="gpt-4o"),
        tools=[
            DuckDuckGoTools(),
            PythonTools(),
            save_html_tool
        ],
        instructions=[
            "You will be given the name of a board member and a list of their interests.",
            "Use DuckDuckGo to search for site:Crowe.com + each interest keyword to find relevant articles.",
            "Summarize or rephrase key insights from these articles and personalize them for the given individual.",
            "Structure the final output as a full standalone HTML page and use SaveHTMLTool to save it with the filename (e.g., darren-walker.html).",
            "Do NOT print or include the HTML content in your response. Just confirm the save.",
            "Respond only with a success message and the correct public URL: http://172.178.45.177:8080/<filename>. Do not mention localhost or port 3000.",
            "Be concise. Avoid repeating steps already completed. Your response should only contain the public link and confirmation."
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
