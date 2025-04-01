from duckduckgo_search import DDGS
from agno.tools.function import FunctionTool
from threading import Lock
import json

class LimitedDuckDuckGo:
    def __init__(self, max_calls=3):
        self.call_count = 0
        self.max_calls = max_calls
        self.lock = Lock()

    def duckduckgo_search_limited(self, query: str, max_results: int = 5) -> str:
        with self.lock:
            if self.call_count >= self.max_calls:
                raise RuntimeError("DuckDuckGo limit exceeded: max 3 queries allowed.")
            self.call_count += 1

        try:
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=max_results)
                return json.dumps(results, indent=2)
        except Exception as e:
            raise RuntimeError(f"DuckDuckGo search failed: {str(e)}")

    def get_tool(self):
        return FunctionTool.from_function(
            name="duckduckgo_search",
            description="Searches the web using DuckDuckGo (limited to 3 total calls per agent run).",
            entrypoint=self.duckduckgo_search_limited
        )
