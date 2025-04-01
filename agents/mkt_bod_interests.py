from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage

from agno.tools.wikipedia import WikipediaTools
from agno.tools.python import PythonTools
from tools.limited_duckduckgo import LimitedDuckDuckGo

def create_bod_interests_agent():
    return Agent(
        name="mkt_bod_interests",
        description=(
            "Identifies interests and public posts of board members using limited web search (DuckDuckGo) "
            "and knowledge bases (Wikipedia)."
        ),
        model=OpenAIChat(id="gpt-4o"),
        tools=[
            LimitedDuckDuckGo(max_calls=3).get_tool(),
            WikipediaTools(),
            PythonTools()
        ],
        instructions=[
            "You will receive the name of a board member.",
            "Use DuckDuckGo to retrieve **at most 3 total queries per run**. Combine keywords wisely.",
            "Prefer queries that include their name plus keywords like 'LinkedIn', 'interview', 'leadership', 'keynote', or company affiliation.",
            "From search results, extract direct quotes, post summaries, or article excerpts that reflect real, verifiable interests.",
            "Use Wikipedia **only if DuckDuckGo fails** or no usable info is found, and only when a detailed biography exists.",
            "Clearly label your sources with [DuckDuckGo], [Wikipedia], or [Other] and include working URLs.",
            "Never fabricate information. Use only verifiable sources.",
            "Finish with a **bullet-point list of inferred interests**, based on actual content, not assumptions."
        ],
        show_tool_calls=True,
        markdown=True,
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        storage=SqliteAgentStorage(
            table_name="bod_interests",
            db_file="tmp/agents.db"
        )
    )
