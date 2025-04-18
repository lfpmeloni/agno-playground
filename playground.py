from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from agno.playground import Playground, serve_playground_app
from agents.exp_web_agent import web_agent
from agents.exp_finance_agent import finance_agent
from agents.mkt_board_of_directors import create_board_agent
from agents.mkt_bod_interests import create_bod_interests_agent
from agents.mkt_content_generator import create_content_generator_agent
from agents.hr_quarter_review import create_quarterly_review_agent

# SQLite path
agent_storage = "tmp/agents.db"

# Playground app definition
app = Playground(
    agents=[
        web_agent,
        finance_agent,
        create_board_agent(),
        create_bod_interests_agent(),
        create_content_generator_agent(),
        create_quarterly_review_agent()
    ]
).get_app()

# Allow CORS for external browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check route
@app.get("/v1/playground/status")
async def playground_status():
    return JSONResponse(content={"status": "ok"})

# Start the app
if __name__ == "__main__":
    serve_playground_app("playground:app", host="0.0.0.0", port=7777, reload=True)