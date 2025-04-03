from flask import Flask, render_template, send_from_directory
import os

app = Flask(__name__, template_folder="frontend/templates")

# Static HTML folder (generated insights pages)
STATIC_PAGES_DIR = os.path.abspath("static_pages")

@app.route("/")
def home():
    return render_template("entrypoint.html")

@app.route("/parent-agent")
def parent_agent_ui():
    return render_template("index.html")

@app.route("/static-pages/<path:filename>")
def static_pages(filename):
    return send_from_directory(STATIC_PAGES_DIR, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
