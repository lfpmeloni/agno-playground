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
            DuckDuckGoTools(),
            WikipediaTools(),
            PythonTools()
        ],
        instructions=[
            "Use DuckDuckGo to retrieve at least 10 search results related to the person's LinkedIn profile and public posts.",
            "From those, extract *specific posts, quotes, or activity descriptions*. Always provide the full URL for each finding.",
            "Use Wikipedia only if a detailed biography exists. Label your findings clearly as [LinkedIn], [Wikipedia], or [Other].",
            "DO NOT invent information. Use ONLY what is verifiable from tools.",
            "Label each section: [LinkedIn], [Wikipedia], [Other]"
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
