from flask import Flask, render_template, request
import subprocess
import threading
import uuid

app = Flask(__name__)

# Store running output for simplicity
outputs = {}

def run_team_agent(team_name, prompt, job_id):
    try:
        # Dynamically call the marketing_team script with the prompt as an env var
        result = subprocess.run(
            ['python3', f'teams/{team_name}.py', prompt], capture_output=True, text=True
        )
        outputs[job_id] = result.stdout
    except Exception as e:
        outputs[job_id] = f"Error running script: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_agent = request.form['agent']
        prompt = request.form['prompt']
        job_id = str(uuid.uuid4())

        # Start background task
        thread = threading.Thread(target=run_team_agent, args=(selected_agent, prompt, job_id))
        thread.start()

        return render_template('output.html', job_id=job_id, output=None)
    return render_template('index.html')

@app.route('/status/<job_id>')
def check_status(job_id):
    output = outputs.get(job_id)
    return output or "<p><em>Still running...</em></p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
