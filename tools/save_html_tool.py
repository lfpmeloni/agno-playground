import os
from datetime import datetime
from agno.tools import tool

PUBLIC_DIR = os.path.expanduser("~/agno-server/public_pages")
INDEX_PATH = os.path.join(PUBLIC_DIR, "index.html")

# Ensure public_pages directory exists
os.makedirs(PUBLIC_DIR, exist_ok=True)

@tool(name="save_html_file", description="Save an HTML page for a board member and update the public index.")
def save_html_file(name: str, content: str) -> str:
    """
    Save a personalized HTML file under ~/agno-server/public_pages/<name>.html
    and update the index.html file with a link to it.

    Args:
        name (str): The board member's name.
        content (str): Full HTML content for their page.

    Returns:
        str: URL path to the generated HTML file.
    """
    slug = name.lower().replace(" ", "_").replace(".", "")
    filename = f"{slug}.html"
    filepath = os.path.join(PUBLIC_DIR, filename)

    # Wrap in minimal HTML shell if not already
    if "<html" not in content:
        content = f"""
        <!DOCTYPE html>
        <html lang=\"en\">
        <head>
            <meta charset=\"UTF-8\">
            <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
            <link rel=\"stylesheet\" href=\"style.css\">
            <title>{name} – Crowe Insights</title>
        </head>
        <body>
            <h1>{name}</h1>
            {content}
        </body>
        </html>
        """

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    # Update index.html
    links = []
    for file in sorted(os.listdir(PUBLIC_DIR)):
        if file.endswith(".html") and file != "index.html":
            display_name = file.replace("_", " ").replace(".html", "").title()
            links.append(f"<li><a href=\"{file}\">{display_name}</a></li>")

    index_html = f"""
    <!DOCTYPE html>
    <html lang=\"en\">
    <head>
        <meta charset=\"UTF-8\">
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
        <link rel=\"stylesheet\" href=\"style.css\">
        <title>Crowe Insights Dashboard</title>
    </head>
    <body>
        <h1>Crowe Insights Dashboard</h1>
        <p>Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <ul>
            {''.join(links)}
        </ul>
    </body>
    </html>
    """
    with open(INDEX_PATH, "w", encoding="utf-8") as idx:
        idx.write(index_html)

    return f"/public_pages/{filename}"

# OPTIONAL: create a style.css if not already present
style_path = os.path.join(PUBLIC_DIR, "style.css")
if not os.path.exists(style_path):
    with open(style_path, "w", encoding="utf-8") as f:
        f.write("""
        body {
            font-family: sans-serif;
            margin: 2rem;
            background-color: #f8f8f8;
            color: #333;
        }
        h1 { color: #003366; }
        a { color: #0055aa; text-decoration: none; }
        a:hover { text-decoration: underline; }
        """)
