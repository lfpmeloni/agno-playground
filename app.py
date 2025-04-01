from flask import Flask, render_template
import subprocess

app = Flask(__name__)

@app.route('/')
def run_script():
    result = subprocess.run(
        ['python3', '-m', 'teams.marketing_team'],
        capture_output=True,
        text=True,
        cwd='.',  # ensures it runs from the project root
    )
    output = result.stdout + "\n" + result.stderr
    return render_template('output.html', output=output)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
