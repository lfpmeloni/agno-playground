from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage

# Built-in tools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from agno.tools.wikipedia import WikipediaTools
from agno.tools.python import PythonTools

def create_bod_interests_agent():
    return Agent(
        name="mkt_bod_interests",
        model=OpenAIChat(id="gpt-4o"),
        tools=[
            DuckDuckGoTools(),
            YFinanceTools(company_info=True),
            WikipediaTools(),
            PythonTools()
        ],
        instructions=[
            "You are an interest-finder agent. Your job is to research a person and return a list of interests based on their public online presence.",
            "Use DuckDuckGo to search for LinkedIn, blog posts, bios, or interviews.",
            "Use Wikipedia if the person is public enough to be listed.",
            "Use YFinance to fetch any professional info if they're listed.",
            "Extract key interests such as 'innovation', 'AI', 'sustainability', etc.",
            "Use the Python tool if you need to extract specific patterns from web pages or results.",
            "Be concise and return a bullet-point list of interests with brief context."
        ],
        storage=SqliteAgentStorage(
            table_name="bod_interests",
            db_file="tmp/agents.db"
        ),
        markdown=True,
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5
    )
