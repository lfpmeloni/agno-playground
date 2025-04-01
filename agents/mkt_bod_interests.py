from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage

from agno.tools.wikipedia import WikipediaTools
from agno.tools.python import PythonTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.tavily import TavilyTools

def create_bod_interests_agent():
    return Agent(
        name="mkt_bod_interests",
        description=(
            "Identifies interests and public posts of board members using limited web search (DuckDuckGo, Google, Tavily) "
            "and knowledge bases (Wikipedia)."
        ),
        model=OpenAIChat(id="gpt-4o"),
        tools=[
            DuckDuckGoTools(),
            GoogleSearchTools(),
            TavilyTools(),
            WikipediaTools(),
            PythonTools()
        ],
        instructions=[
            "You will receive the name of a board member.",
            "Use DuckDuckGo for a **single query** to retrieve relevant information. If DuckDuckGo fails, try Google Search, and then Tavily as a last resort.",
            "Combine keywords wisely, such as name + 'LinkedIn', 'interview', 'leadership', or company name.",
            "From search results, extract direct quotes or summaries that reflect real, verifiable interests.",
            "Use Wikipedia only if all search tools fail or give no useful data.",
            "Label all sources as [DuckDuckGo], [Google], [Tavily], or [Wikipedia], and include URLs.",
            "Never fabricate information. Only return actual verified or strongly inferred content.",
            "Finish with a bullet-point list of inferred interests based on retrieved information."
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