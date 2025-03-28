from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage

from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.wikipedia import WikipediaTools
from agno.tools.python import PythonTools  # For parsing and logic, if needed

def create_bod_interests_agent():
    return Agent(
        name="mkt_bod_interests",
        description=(
            "Identifies interests and public posts of board members using "
            "search tools (DuckDuckGo) and knowledge bases (Wikipedia)."
        ),
        model=OpenAIChat(id="gpt-4o"),
        tools=[
            DuckDuckGoTools(num_results=10),
            WikipediaTools(),
            PythonTools()
        ],
        instructions=[
            "Search for the person's LinkedIn profile using DuckDuckGo. Then extract and summarize *specific posts or quotes* using DuckDuckGo snippets. Always provide source URLs for verification.",
            "Use Wikipedia only if it includes a full biography. If not, explain clearly.",
            "NEVER invent quotes or make assumptions. Use ONLY what is verifiable from tools. Label each section: [LinkedIn], [Wikipedia], [Other]"
        ],
        show_tool_calls=True,
        show_reasoning=True,
        markdown=True,
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        storage=SqliteAgentStorage(
            table_name="bod_interests",
            db_file="tmp/agents.db"
        )
    )
