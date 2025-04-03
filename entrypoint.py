# entrypoint.py
from flask import Flask, render_template
import subprocess
import threading
import os

app = Flask(__name__, template_folder="frontend/templates")

# Start Agent UI (needs to run via subprocess in background)
def run_agent_ui():
    os.chdir("agno-server/agent-ui")
    subprocess.run(["pnpm", "start"])

# Start Playground (Agent registration API)
def run_playground():
    os.chdir("agno-server")
    subprocess.run(["python3", "playground.py"])

# Start Parent Agent UI
def run_parent_agent_ui():
    os.chdir("frontend")
    subprocess.run(["python3", "app.py"])

@app.route('/')
def index():
    return render_template("entrypoint.html")

if __name__ == '__main__':
    # Start services in background threads
    threading.Thread(target=run_playground, daemon=True).start()
    threading.Thread(target=run_parent_agent_ui, daemon=True).start()
    threading.Thread(target=run_agent_ui, daemon=True).start()

    # Run entrypoint Flask app
    app.run(host='0.0.0.0', port=5000)
