from agno.tools import tool
from dotenv import load_dotenv
import os
import requests

from tools.wrappers import ToolResult  # Make sure this import path matches your project

@tool
def get_board_of_directors(ticker: str) -> ToolResult:
    """
    Retrieve board of directors for a given company ticker using SEC API.
    """
    load_dotenv()

    api_key = os.getenv("SEC_API_KEY")
    if not api_key:
        return ToolResult("SEC_API_KEY not found in environment.")

    url = f"https://api.sec-api.io/directors-and-board-members?token={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "query": f"ticker:{ticker}",
        "from": 0,
        "size": 10,
        "sort": [{"filedAt": {"order": "desc"}}]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        return ToolResult(f"API error: {e}")

    data = response.json().get("data", [])
    if not data:
        return ToolResult(f"No board members found for {ticker}.")

    output = f"Board of Directors for {ticker}:\n\n"
    for entry in data:
        for director in entry.get("directors", []):
            name = director.get("name", "N/A")
            position = director.get("position", "N/A")
            output += f"• {name} - {position}\n"

    return ToolResult(output)
