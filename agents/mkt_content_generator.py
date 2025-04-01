from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.python import PythonTools
from tools.save_html_tool import save_html_tool

def create_content_generator_agent():
    return Agent(
        name="mkt_content_generator",
        description="Generates personalized HTML content using Crowe.com articles based on the interests of a board member.",
        model=OpenAIChat(id="gpt-4o"),
        tools=[
            DuckDuckGoTools(),
            GoogleSearchTools(),
            PythonTools(),
            save_html_tool
        ],
        instructions=[
            "You will receive the name of a board member and a list of their verified or inferred interests.",
            "Search Crowe.com using a combined query like: site:Crowe.com <interest 1> AND <interest 2>.",
            "Use DuckDuckGo first, then GoogleSearchTools as fallback if needed.",
            "Extract key insights from the articles. Always cite the source with a working clickable link at the end of each paragraph (use <a href=...> format).",
            "Do not fabricate sources. Use only real URLs returned by the tools.",
            "Organize content into three sections: Personal Interests, Recent Activities, and Business Insights.",
            "Build a clean HTML page that embeds links next to each insight.",
            "Save the page using SaveHTMLTool using this format: 'first_last_insights.html'.",
            "After saving the HTML, call update_index() with the filename to ensure the index.html is always up to date.",
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