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
            "Use DuckDuckGo to retrieve at least 10 search results related to the person's LinkedIn profile and public posts.",
            "From those, extract *specific quotes, post summaries, or article snippets* that reflect what this person is interested in — e.g. innovation, healthcare, education, policy, etc.",
            "Clearly list inferred interests based on evidence from their activities or writings.",
            "Use Wikipedia only if a detailed biography exists. Label your findings as [LinkedIn], [Wikipedia], or [Other].",
            "DO NOT invent information. Use ONLY verifiable content. Always include source URLs.",
            "Conclude with a bullet list of verified interests."
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
