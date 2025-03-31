from agno.workflow import Workflow
from agno.run.response import RunResponse, RunEvent
from agno.models.openai import OpenAIChat
from agno.agent import Agent
from agno.utils.log import logger
from agents.mkt_board_of_directors import mkt_board_of_directors
from agents.mkt_bod_interests import mkt_bod_interests
from agents.mkt_content_generator import mkt_generate_webpage_agent

from typing import List
from pydantic import BaseModel

class PersonalizedMarketingWorkflow(Workflow):
    description: str = "Generates a personalized insights webpage for Board Members of a given company based on SEC filings and Crowe.com articles."

    # Step 1: Get Board Members from SEC
    board_extractor: Agent = mkt_board_of_directors

    # Step 2: Enrich board member interests
    interest_enricher: Agent = mkt_bod_interests

    # Step 3: Content generation with Crowe insights
    webpage_generator: Agent = mkt_generate_webpage_agent

    def run(self, ticker_or_name: str) -> RunResponse:
        logger.info(f"🎯 Starting workflow for {ticker_or_name}")

        # Step 1: Get Board Members
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
