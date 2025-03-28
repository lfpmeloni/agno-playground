from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage
from agno.tools.duckduckgo import DuckDuckGoTools


def create_board_agent():
    return Agent(
        name="Board Of Directors",
        model=OpenAIChat(id="gpt-4o"),
        tools=[DuckDuckGoTools()],
        instructions=[
            "Search and extract information about PepsiCo's board of directors using public sources like the SEC."
        ],
        storage=SqliteAgentStorage(table_name="board_directors_agent", db_file="tmp/agents.db"),
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5,
        markdown=True,
    )