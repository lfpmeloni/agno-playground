import os
from dotenv import load_dotenv
import requests

load_dotenv()

class SECAPITool:
    name = "SECAPITool"
    description = (
        "Call the SEC Directors and Board Members API to retrieve directors of a public company given its ticker symbol"
    )

    def run(self, query: str) -> str:
        try:
            api_key = os.getenv("SEC_API_KEY")
            if not api_key:
                return "SEC_API_KEY is not set in environment."

            url = f"https://api.sec-api.io/directors-and-board-members?token={api_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "query": f"ticker:{query.strip().upper()}",
                "from": 0,
                "size": 10,
                "sort": [{"filedAt": {"order": "desc"}}]
            }

            response = requests.post(url, json=payload, headers=headers)

            if response.status_code != 200:
                return f"Failed to fetch data. Status code: {response.status_code}, body: {response.text}"

            data = response.json().get("data", [])
            if not data:
                return "No board of directors found for that company."

            output = []
            for record in data:
                entity = record.get("entityName", "Unknown Company")
                for director in record.get("directors", []):
                    output.append(f"\n### {director.get('name')}\n"
                                  f"- **Position**: {director.get('position', 'N/A')}\n"
                                  f"- **Age**: {director.get('age', 'N/A')}\n"
                                  f"- **Independent**: {director.get('isIndependent', 'Unknown')}\n"
                                  f"- **Committee Memberships**: {', '.join(director.get('committeeMemberships', [])) or 'None'}\n"
                                  f"- **Experience**: {', '.join(director.get('qualificationsAndExperience', [])) or 'Not listed'}\n")

            return f"## Board of Directors for {entity}:\n" + "\n".join(output)

        except Exception as e:
            return f"An error occurred: {str(e)}"