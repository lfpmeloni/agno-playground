import sys
import argparse
import asyncio
import os

from agno.workflow import Workflow
from agno.models.openai import OpenAIChat
from agno.utils.log import logger
from agno.storage.sqlite import SqliteStorage

from agents.mkt_board_of_directors import create_board_agent
from agents.mkt_bod_interests import create_bod_interests_agent
from agents.mkt_content_generator import create_content_generator_agent

from agno.agent import Agent
from agno.run.response import RunResponse, RunEvent

class PersonalizedMarketingWorkflow(Workflow):
    description: str = "Generates a personalized insights webpage for Board Members of a given company based on SEC filings and Crowe.com articles."

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.board_extractor: Agent = create_board_agent()
        self.interest_enricher: Agent = create_bod_interests_agent()
        self.webpage_generator: Agent = create_content_generator_agent()

    async def run_workflow(self, ticker_or_name: str) -> RunResponse:
        logger.info(f"🎯 Starting workflow for {ticker_or_name}")

        logger.info("🔍 Fetching Board Members from SEC...")
        board_response = await self.board_extractor.arun(ticker_or_name)
        names = board_response.content if isinstance(board_response.content, list) else []

        if not names:
            return RunResponse(content="⚠️ No board members found.", event=RunEvent.workflow_completed)

        final_outputs = []
        for name in names:
            logger.info(f"🎯 Finding interests for {name}")
            interests_response = await self.interest_enricher.arun(name)

            enriched_input = {
                "name": name,
                "interests": interests_response.content
            }

            logger.info(f"🌐 Generating personalized page for {name}...")
            generation_response = await self.webpage_generator.arun(enriched_input)
            final_outputs.append(f"{name}: {generation_response.content}")

        summary = "\n\n".join(final_outputs)
        return RunResponse(
            content=summary,
            event=RunEvent.workflow_completed
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Personalized Marketing Workflow")
    parser.add_argument(
        "--ticker",
        type=str,
        default="PEP",
        help="Company ticker or name (e.g., PEP, PepsiCo)"
    )
    args = parser.parse_args()

    workflow = PersonalizedMarketingWorkflow(
        workflow_id="mkt-orchestration-cli",
        storage=SqliteStorage(
            table_name="mkt_orchestration_workflow",
            db_file="tmp/agno_workflows.db"
        )
    )

    result = asyncio.run(workflow.run_workflow(args.ticker))
    print("\n✅ Final Output:\n")
    print(result.content or "⚠️ No output generated.")
