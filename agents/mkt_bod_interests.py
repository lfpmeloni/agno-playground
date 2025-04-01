from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage

from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.wikipedia import WikipediaTools
from agno.tools.python import PythonTools

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
            "You will receive the name of a board member.",
            "Use DuckDuckGo to retrieve at most **3 queries total** (not more than 3 tool calls). Choose your queries wisely.",
            "Prioritize searches for LinkedIn, recent interviews, or thought leadership articles.",
            "From those results, extract *specific quotes, post summaries, or article snippets* that reflect what this person is interested in — e.g. innovation, healthcare, education, policy, etc.",
            "Use Wikipedia only if a detailed biography exists and DuckDuckGo yields little or no useful information.",
            "Label each finding with [DuckDuckGo], [Wikipedia], or [Other] and include source URLs.",
            "DO NOT invent information. Use ONLY verifiable content.",
            "Conclude with a bullet list of verified or strongly inferred interests based on retrieved data."
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
