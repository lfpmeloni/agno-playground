from flask import Flask, render_template
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def run_team_script():
    # Absolute path to your script
    script_path = os.path.abspath('teams/marketing_team.py')

    # Run script using subprocess, capturing both stdout and stderr
    result = subprocess.run(['python3', script_path], capture_output=True, text=True)
    output = result.stdout + '\n' + result.stderr  # Include errors in output if any

    return render_template('output.html', output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
