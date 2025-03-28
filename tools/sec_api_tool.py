from agno.tools import tool
from dotenv import load_dotenv
import os

@tool
def get_board_of_directors(ticker: str) -> str:
    """
    Retrieve board of directors for a given company ticker using SEC API.
    """
    import os, requests

    load_dotenv()

    api_key = os.getenv("SEC_API_KEY")
    if not api_key:
        return "SEC_API_KEY not found in environment."

    url = f"https://api.sec-api.io/directors-and-board-members?token={api_key}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "query": f"ticker:{ticker}",
        "from": 0,
        "size": 10,
        "sort": [{"filedAt": {"order": "desc"}}]
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code != 200:
        return f"API error: {response.status_code} - {response.text}"

    data = response.json().get("data", [])
    if not data:
        return f"No board members found for {ticker}."

    output = f"Board of Directors for {ticker}:\n"
    for entry in data:
        for director in entry.get("directors", []):
            output += f"- {director['name']} ({director.get('position', 'N/A')})\n"
    return output