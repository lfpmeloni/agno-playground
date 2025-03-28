from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools.duckduckgo import DuckDuckGoTools


def create_bod_interests_agent():
    return Agent(
        name="BOD Interests",
        model=OpenAIChat(id="gpt-4o"),
        tools=[DuckDuckGoTools()],
        instructions=[
            "Given a board member's name, find recent public content (e.g., LinkedIn, articles) to infer their personal and professional interests."
        ],
        storage=SqliteAgentStorage(table_name="bod_interests_agent", db_file="tmp/agents.db"),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=True,
    )