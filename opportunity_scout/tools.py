from tavily import TavilyClient
from config import TAVILY_API_KEY


def tavily_search(query: str, max_results: int = 5) -> str:
    client = TavilyClient(api_key=TAVILY_API_KEY)
    response = client.search(
        query=query,
        max_results=max_results,
        search_depth="advanced",
    )

    results = response.get("results", [])
    if not results:
        return "No results found for this query."

    parts = []
    for i, r in enumerate(results, 1):
        parts.append(
            f"Result {i}:\n"
            f"  Title: {r.get('title', 'N/A')}\n"
            f"  URL: {r.get('url', 'N/A')}\n"
            f"  Published: {r.get('published_date', 'N/A')}\n"
            f"  Content: {r.get('content', 'N/A')}\n"
        )
    return "\n---\n".join(parts)


# Anthropic tool definition
TOOLS = [
    {
        "name": "web_search",
        "description": (
            "Search the web for current internship, fellowship, and grant opportunities "
            "for African university students. Always run several targeted searches to cover "
            "different opportunity types (internships, fellowships, grants) and different "
            "organizations (NGOs, governments, universities, companies)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "A specific search query. Examples: "
                        "'internships for African computer science students 2025', "
                        "'fellowships open to African students engineering 2025', "
                        "'grants for African university students research 2025'."
                    ),
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of search results to return. Default is 5.",
                },
            },
            "required": ["query"],
        },
    }
]


def execute_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "web_search":
        return tavily_search(
            query=tool_input["query"],
            max_results=tool_input.get("max_results", 5),
        )
    return f"Unknown tool: {tool_name}"
