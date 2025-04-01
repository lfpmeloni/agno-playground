from flask import Flask, render_template, request, redirect, url_for
import threading
import uuid
import asyncio
from teams.marketing_team import get_marketing_team

app = Flask(__name__)

# Store running output and job status
outputs = {}
running_jobs = set()
team_instance = get_marketing_team()

# Async function to run agent and stream output to terminal + store
async def run_team_agent(prompt, job_id):
    outputs[job_id] = "Task started...\n"

    async def stream_output(chunk):
        print(chunk, end="", flush=True)  # Print to terminal in real-time
        outputs[job_id] += chunk

    try:
        print(f"\n🔁 Running marketing_team with job_id: {job_id}\n")
        await team_instance.aprint_response(
            message=prompt,
            stream=True,
            stream_intermediate_steps=True,
            callback=stream_output
        )
        outputs[job_id] += "\n✅ Done!"
    except Exception as e:
        print(f"❌ Error in job {job_id}: {e}")
        outputs[job_id] += f"\n❌ Error: {e}"
    finally:
        running_jobs.discard(job_id)

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
    return render_template('output.html', job_id=job_id, output=output or "<p><em>Still running...</em></p>", dark_mode=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
