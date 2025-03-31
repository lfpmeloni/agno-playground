from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from workflows.mkt_orchestration import PersonalizedMarketingWorkflow
from agno.storage.sqlite import SqliteStorage

app = FastAPI()

@app.get("/run-marketing", response_class=HTMLResponse)
async def run_marketing_workflow(request: Request):
    try:
        workflow = PersonalizedMarketingWorkflow(
            workflow_id="marketing-orchestration-ui",
            storage=SqliteStorage(
                table_name="marketing_ui_storage",
                db_file="tmp/agno_workflows.db"
            )
        )

        # Replace this with whatever default input you want to use
        ticker_or_company = "PEP"
        response = workflow.run(ticker_or_company)

        content = response.content if response and response.content else "No output generated."

        return f"""
        <html>
            <head>
                <title>Marketing Workflow Output</title>
                <style>
                    body {{ font-family: monospace; padding: 20px; background: #111; color: #0f0; }}
                    pre {{ white-space: pre-wrap; word-wrap: break-word; }}
                    a {{ color: cyan; }}
                </style>
            </head>
            <body>
                <h1>📄 Workflow Output for <code>{ticker_or_company}</code></h1>
                <pre>{content}</pre>
                <br><a href="/run-marketing">🔁 Run again</a>
            </body>
        </html>
        """
    except Exception as e:
        return HTMLResponse(content=f"<h1>❌ Error</h1><pre>{str(e)}</pre>", status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("terminal_ui:app", host="0.0.0.0", port=8000, reload=True)
