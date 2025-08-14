from fastmcp import FastMCP
from src.semantic_search import semantic_search_commits

# Create a server instance
mcp = FastMCP(name="GithubOrgExplorer")


# @mcp.tool
# def info() -> str:
#     """Provides information about the tool."""
#     return "This is a tool for exploring GitHub organizations."


@mcp.tool
def find_interesting_commits(commit_type: str):
    """
    Find interesting commits based on the specified commit type. It shows the reason why and specific code examples that are useful for the developer.
    """
    results = semantic_search_commits(commit_type, top_k=3)
    for result in results:
        print(f"Found commit: {result['title']} (Similarity: {result['similarity']})")
    return results


if __name__ == "__main__":
    mcp.run()
