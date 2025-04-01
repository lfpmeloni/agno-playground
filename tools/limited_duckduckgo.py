from agno.tools.duckduckgo import duckduckgo_search
from agno.tools.function import FunctionTool
from threading import Lock

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
        return duckduckgo_search(query=query, max_results=max_results)

    def get_tool(self):
        return FunctionTool.from_function(
            name="duckduckgo_search",
            description="Searches the web using DuckDuckGo with a strict limit of 3 queries.",
            entrypoint=self.duckduckgo_search_limited
        )
