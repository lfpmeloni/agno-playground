import os
from datetime import datetime
from agno.tools import tool

PUBLIC_DIR = os.path.join(os.path.dirname(__file__), "../public")
os.makedirs(PUBLIC_DIR, exist_ok=True)

@tool(name="SaveHTMLTool", description="Save a personalized HTML file and update the index page")
def save_html_tool(name: str, html_content: str) -> str:
    name_slug = name.lower().replace(" ", "-").replace(".html", "")
    filename = f"{name_slug}.html"
    filepath = os.path.join(PUBLIC_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    index_path = os.path.join(PUBLIC_DIR, "index.html")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    link_entry = f'<li><a href="{filename}">{name}</a> - Updated on {now}</li>\n'

    if not os.path.exists(index_path):
        with open(index_path, "w", encoding="utf-8") as index:
            index.write("<html><head><link rel='stylesheet' href='style.css'></head><body><h1>Generated Pages</h1><ul>\n")
            index.write(link_entry)
            index.write("</ul></body></html>")
    else:
        with open(index_path, "r+", encoding="utf-8") as index:
            content = index.read()
            if filename not in content:
                updated_content = content.replace("</ul>", link_entry + "</ul>")
                index.seek(0)
                index.write(updated_content)
                index.truncate()

    return f"Saved HTML for {name} to {filename} and updated index."
