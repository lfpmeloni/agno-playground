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

# Global dictionaries to store job outputs, metadata, and active jobs per agent
outputs = {}
# jobs_meta maps job_id to metadata (e.g. {"agent": "marketing_team"})
jobs_meta = {}
# active_jobs_by_agent maps an agent to its currently running job id
active_jobs_by_agent = {}
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

        # Append any captured stdout after completion
        clean_stdout = ansi_escape.sub('', f.getvalue())
        outputs[job_id] += clean_stdout
        outputs[job_id] += "\n✅ Task completed successfully.\n"

    except Exception as e:
        outputs[job_id] += f"\n❌ Error: {e}"
    finally:
        running_jobs.discard(job_id)
        outputs[job_id] += "\n🏁 Job finished.\n"
        # Remove the active job mapping for this agent if it is the same job id
        agent = jobs_meta.get(job_id, {}).get("agent")
        if agent in active_jobs_by_agent and active_jobs_by_agent[agent] == job_id:
            del active_jobs_by_agent[agent]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        agent = request.form.get("agent")
        prompt = request.form.get("prompt")
        if not prompt:
            return render_template("index.html", error="Prompt cannot be empty.")

        # If a job for this agent is already running, redirect to that status page
        existing_job = active_jobs_by_agent.get(agent)
        if existing_job and existing_job in outputs and "🏁 Job finished." not in outputs[existing_job]:
            return redirect(url_for('check_status', job_id=existing_job))

        try:
            team_instance = load_team(agent)
        except ValueError as e:
            return render_template("index.html", error=str(e))
        job_id = str(uuid.uuid4())
        jobs_meta[job_id] = {"agent": agent}
        active_jobs_by_agent[agent] = job_id
        threading.Thread(
            target=lambda: asyncio.run(run_team_agent(prompt, job_id, team_instance))
        ).start()
        return redirect(url_for('check_status', job_id=job_id))
    return render_template("index.html")

@app.route('/status/<job_id>')
def check_status(job_id):
    output = outputs.get(job_id)
    done = output and ("✅ Task completed" in output or "❌ Error" in output or "🏁 Job finished." in output)

    # For AJAX polling requests, return plain text output
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return output or "Still running..."

    # Use stored metadata for header (or default to a generic header)
    job_meta = jobs_meta.get(job_id, {})
    agent = job_meta.get("agent", "")
    if agent == "marketing_team":
         header = "Marketing Team Output"
    elif agent == "hr_team_coordinator":
         header = "HR Review Team Output"
    else:
         header = "Agent Output"

    return render_template(
        'output.html',
        job_id=job_id,
        output=output or "Still running...",
        dark_mode=True,
        done=done,
        agent_name=header
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
