import os
from dotenv import load_dotenv
import requests

load_dotenv()

class SECAPITool:
    name = "SECAPITool"
    description = "Fetch Board of Directors using SEC API based on ticker symbol."

    def run(self, query: str) -> str:
        try:
            api_key = os.getenv("SEC_API_KEY")
            if not api_key:
                return "SEC_API_KEY is not set in environment."

            base_url = "https://api.sec-api.io/directors"
            params = {
                "companyTicker": query.strip(),
                "appKey": api_key
            }

            response = requests.get(base_url, params=params)

            if response.status_code == 200:
                data = response.json()
                if not data.get("data"):
                    return "No board of directors found for that company."

                output = []
                for director in data["data"]:
                    output.append(
                        f"- **{director.get('name')}** — {director.get('position', 'N/A')} at {director.get('companyName', 'Unknown')}"
                    )

                return "\n".join(output)

            return f"Failed to fetch data. Status code: {response.status_code}"
        except Exception as e:
            return f"An error occurred: {str(e)}"
