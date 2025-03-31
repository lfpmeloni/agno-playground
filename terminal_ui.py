from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from workflows.mkt_orchestration import PersonalizedMarketingWorkflow
from agno.storage.sqlite import SqliteStorage

app = FastAPI()

@app.get("/run-marketing", response_class=HTMLResponse)
async def run_marketing_workflow(request: Request, ticker: str = "PEP"):
    try:
        workflow = PersonalizedMarketingWorkflow(
            workflow_id="marketing-orchestration-ui",
            storage=SqliteStorage(
                table_name="marketing_ui_storage",
                db_file="tmp/agno_workflows.db"
            )
        )

        response = workflow.run_workflow(ticker)
        content = response.content if response and response.content else "No output generated."

        return f"""
        <html>
            <head>
                <title>Marketing Workflow Output</title>
                <style>
                    body {{ font-family: monospace; padding: 20px; background: #111; color: #0f0; }}
                    input[type='text'] {{ padding: 4px; font-size: 14px; }}
                    button {{ margin-left: 10px; padding: 4px 10px; }}
                    pre {{ white-space: pre-wrap; word-wrap: break-word; }}
                    a {{ color: cyan; }}
                </style>
            </head>
            <body>
                <h1>📄 Workflow Output for <code>{ticker}</code></h1>
                <form method="get" action="/run-marketing">
                    <label>Enter ticker: </label>
                    <input type="text" name="ticker" value="{ticker}" />
                    <button type="submit">▶️ Run</button>
                </form>
                <pre>{content}</pre>
            </body>
        </html>
        """
    except Exception as e:
        return HTMLResponse(content=f"<h1>❌ Error</h1><pre>{str(e)}</pre>", status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("terminal_ui:app", host="0.0.0.0", port=8000, reload=True)
