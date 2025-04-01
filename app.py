from flask import Flask, render_template, request, redirect, url_for, render_template_string
import threading
import re
import io
import uuid
import asyncio
from contextlib import redirect_stdout
from teams.marketing_team import get_marketing_team

app = Flask(__name__)

ansi_escape = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')

# Store running output and job status
outputs = {}
running_jobs = set()
team_instance = get_marketing_team()

async def run_team_agent(prompt, job_id):
    outputs[job_id] = "🔁 Task started...\n"

    f = io.StringIO()

    async def stream_output(chunk):
        # Also capture what Agno gives directly
        print(chunk, end="", flush=True)
        clean_chunk = ansi_escape.sub('', chunk)
        outputs[job_id] += clean_chunk

    try:
        print(f"\n🔁 Running marketing_team with job_id: {job_id}\n")
        running_jobs.add(job_id)

        with redirect_stdout(f):  # Capture everything printed to terminal
            await team_instance.aprint_response(
                message=prompt,
                stream=True,
                stream_intermediate_steps=True,
                callback=stream_output
            )

        # Append captured stdout after the agent finishes
        outputs[job_id] += f.getvalue()
        outputs[job_id] += "\n✅ Task completed successfully.\n"

    except Exception as e:
        outputs[job_id] += f"\n❌ Error: {e}"
    finally:
        running_jobs.discard(job_id)
        outputs[job_id] += "\n🏁 Job finished.\n"

# Route to submit job and start background async task
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

# Status route to check job output
@app.route('/status/<job_id>')
def check_status(job_id):
    output = outputs.get(job_id)
    done = output and ("✅ Task completed" in output or "❌ Error" in output or "🏁 Job finished." in output)

    # When request comes from AJAX, return just the raw string
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
