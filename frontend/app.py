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


app = Flask(__name__)

# Regex to remove ANSI escape sequences (e.g., colors)
ansi_escape = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')

# Store job outputs and status
outputs = {}
running_jobs = set()
team_instance = get_marketing_team()

async def run_team_agent(prompt, job_id):
    outputs[job_id] = "🔁 Task started...\n"
    f = io.StringIO()

    async def stream_output(chunk):
        clean_chunk = ansi_escape.sub('', chunk)
        outputs[job_id] += clean_chunk
        print(chunk, end="", flush=True)

    try:
        print(f"\n🔁 Running marketing_team with job_id: {job_id}\n")
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        prompt = request.form['prompt']
        job_id = str(uuid.uuid4())

        if job_id in running_jobs:
            return redirect(url_for('check_status', job_id=job_id))

        running_jobs.add(job_id)

        def start_async_task():
            asyncio.run(run_team_agent(prompt, job_id))

        thread = threading.Thread(target=start_async_task)
        thread.start()

        return redirect(url_for('check_status', job_id=job_id))
    return render_template('index.html', dark_mode=True)

@app.route('/status/<job_id>')
def check_status(job_id):
    output = outputs.get(job_id)
    done = output and ("✅ Task completed" in output or "❌ Error" in output or "🏁 Job finished." in output)

    # Handle AJAX polling requests
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return output or "Still running..."

    return render_template(
        'output.html',
        job_id=job_id,
        output=output or "Still running...",
        dark_mode=True,
        done=done
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
