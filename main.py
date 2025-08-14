import json
from src.semantic_search import semantic_search_commits
import asyncio
from fastmcp import FastMCP, Client

# Create a server instance
mcp = FastMCP(name="GithubOrgExplorer")

commit_prompt_template = """
Here are the commits from a tool (JSON array):

{{commits}}

For each commit show the diff(VERY IMPORTANT) and the reason why it's interesting. Don't add etra commentary

Give one last overview in 1 paragraph maximum
"""


@mcp.tool
def find_interesting_commits(commit_type: str):
    """
    Find interesting commits based on the specified commit type. It shows the reason why and specific code examples that are useful for the developer.
    """
    results = semantic_search_commits(commit_type, top_k=3)

    filtered_results = []
    for result in results:
        filtered_result = {
            "diffs": result.get("diffs"),
            "reason": result.get("reason"),
            "repo": result.get("repo"),
        }
        filtered_results.append(filtered_result)
    return commit_prompt_template.replace("{{commits}}", json.dumps(filtered_results))


# client = Client(mcp)


# async def call_tool(name: str):
#     async with client:
#         result = await client.call_tool(
#             "find_interesting_commits", {"commit_type": name}
#         )
#         print(result)


# asyncio.run(call_tool("yaml"))


if __name__ == "__main__":
    mcp.run()
