from flask import Flask, render_template, request, redirect, url_for
import threading
import re
import io
import uuid
import asyncio
from contextlib import redirect_stdout

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from teams.marketing_team import get_marketing_team
from teams.hr_team_coordinator import get_hr_team

def load_team(agent_name):
    if agent_name == "marketing_team":
        return get_marketing_team()
    elif agent_name == "hr_team_coordinator":
        return get_hr_team()
    else:
        raise ValueError(f"Unknown agent name: {agent_name}")

app = Flask(__name__)

# Regex to remove ANSI escape sequences (e.g., colors)
ansi_escape = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')

# Store job outputs and status
outputs = {}
running_jobs = set()

async def run_team_agent(prompt, job_id, team_instance):
    outputs[job_id] = "🔁 Task started...\n"
    f = io.StringIO()

    async def stream_output(chunk):
        clean_chunk = ansi_escape.sub('', chunk)
        outputs[job_id] += clean_chunk
        print(chunk, end="", flush=True)

    try:
        print(f"\n🔁 Running {team_instance.name} with job_id: {job_id}\n")
        running_jobs.add(job_id)

        # Redirect stdout (e.g., print() calls)
        with redirect_stdout(f):
            await team_instance.aprint_response(
                message=prompt,
                stream=True,
                stream_intermediate_steps=True,
                callback=stream_output
            )

        # Clean and append captured stdout after completion
        clean_stdout = ansi_escape.sub('', f.getvalue())
        outputs[job_id] += clean_stdout
        outputs[job_id] += "\n✅ Task completed successfully.\n"

    except Exception as e:
        outputs[job_id] += f"\n❌ Error: {e}"
    finally:
        running_jobs.discard(job_id)
        outputs[job_id] += "\n🏁 Job finished.\n"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        agent = request.form.get("agent")
        prompt = request.form.get("prompt")
        # Process the agent and prompt...
        return render_template("index.html")
    return render_template("index.html")

@app.route('/status/<job_id>')
def check_status(job_id):
    output = outputs.get(job_id)
    done = output and ("✅ Task completed" in output or "❌ Error" in output or "🏁 Job finished." in output)

    # Handle AJAX polling requests
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return output or "Still running..."

    # NEW: infer agent name from output (hacky but works)
    agent_name = "HR Review Team" if "BOLD_GOALS" in output else "Marketing Team"

    return render_template(
        'output.html',
        job_id=job_id,
        output=output or "Still running...",
        dark_mode=True,
        done=done,
        agent_name=agent_name
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
