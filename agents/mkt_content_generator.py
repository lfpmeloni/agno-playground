from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools.duckduckgo import DuckDuckGoTools


def create_content_generator_agent():
    return Agent(
        name="Content Generator",
        model=OpenAIChat(id="gpt-4o"),
        tools=[DuckDuckGoTools()],
        instructions=[
            "Using the interests of a board member and sources like Crowe.com, generate personalized strategic advisory content for display on a dedicated webpage."
        ],
        storage=SqliteAgentStorage(table_name="content_generator_agent", db_file="tmp/agents.db"),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=True,
    )