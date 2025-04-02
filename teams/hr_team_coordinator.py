from agno.team.team import Team
from agno.models.openai import OpenAIChat
from agno.storage.agent.sqlite import SqliteAgentStorage
from agents.hr_feedback_agent import create_feedback_agent
from agents.hr_client_work_agent import create_client_work_agent
from agents.hr_goal_alignment_agent import create_goal_alignment_agent

def get_hr_team():
    return Team(
        name="HR Team Coordinator",
        team_id="hr_team",
        description="Coordinates agents for quarterly employee performance review.",
        model=OpenAIChat("gpt-4o"),
        mode="coordinate",
        members=[
            create_feedback_agent(),
            create_client_work_agent(),
            create_goal_alignment_agent()
        ],
        instructions=[
            "You are the HR coordinator managing a quarterly performance review.",
            "Each member of your team has expertise in feedback analysis, client work, and goal alignment.",
            "Coordinate the review process by assigning each agent to summarize their respective area.",
            "Then consolidate these summaries into one complete performance review report.",
            "Be clear and concise. Format the response with section titles and bullet points."
        ],
        success_criteria="The final response includes insights from all three areas and is formatted as a complete quarterly review.",
        show_tool_calls=True,
        show_members_responses=True,
        enable_agentic_context=True,
        markdown=True,
        storage=SqliteAgentStorage(table_name="hr_team", db_file="tmp/agents.db")
    )
