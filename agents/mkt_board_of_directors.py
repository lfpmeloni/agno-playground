from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage
from tools.sec_api_tool import get_board_of_directors  # ✅ the tool is already registered

def create_board_agent():
    return Agent(
        name="mkt_board_of_directors",
        model=OpenAIChat(id="gpt-4o"),
        tools=[get_board_of_directors],  # ✅ use directly
        description="Use SEC API to find board of directors for a public company based on ticker symbol (e.g., PEP).",
        storage=SqliteAgentStorage(table_name="board_of_directors", db_file="tmp/agents.db"),
        markdown=True,
        add_datetime_to_instructions=True,
        add_history_to_messages=True,
        num_history_responses=5
    )
