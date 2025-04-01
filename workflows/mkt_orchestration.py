from agno.workflow import Workflow
from agno.run.response import RunResponse, RunEvent
from agno.models.openai import OpenAIChat
from agno.agent import Agent
from agno.utils.log import logger
from agents.mkt_board_of_directors import create_board_agent
from agents.mkt_bod_interests import create_bod_interests_agent
from agents.mkt_content_generator import create_content_generator_agent

import argparse
from typing import List
from pydantic import BaseModel

class PersonalizedMarketingWorkflow(Workflow):
    description: str = "Generates a personalized insights webpage for Board Members of a given company based on SEC filings and Crowe.com articles."

    # Step 1: Get Board Members from SEC
    board_extractor: Agent = create_board_agent()

    # Step 2: Enrich board member interests
    interest_enricher: Agent = create_bod_interests_agent()

    # Step 3: Content generation with Crowe insights
    webpage_generator: Agent = create_content_generator_agent()

    def run_workflow(self, ticker_or_name: str) -> RunResponse:
        logger.info(f"🎯 Starting workflow for {ticker_or_name}")

        logger.info("🔍 Fetching Board Members from SEC...")
        board_response = self.board_extractor.run(ticker_or_name)
        names = board_response.content if isinstance(board_response.content, list) else []

        all_interests = []
        for name in names:
            logger.info(f"🎯 Finding interests for {name}")
            interests_response = self.interest_enricher.run(name)
            all_interests.append({
                "name": name,
                "interests": interests_response.content
            })

        logger.info(f"🧠 Generating personalized marketing page with Crowe insights...")
        final_page = self.webpage_generator.run(all_interests)

        return RunResponse(
            content=final_page.content,
            event=RunEvent.workflow_completed
        )

# Run from terminal
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
        storage=None  # Add SqliteStorage if you want persistence
    )

    result = workflow.run_workflow(args.ticker)
    print("\n✅ Final Output:\n")
    print(result.content or "⚠️ No output generated.")