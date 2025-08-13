from fastmcp import FastMCP

# Create a server instance
mcp = FastMCP(name="GithubOrgExplorer")


@mcp.tool
def info() -> str:
    """Provides information about the tool."""
    return "This is a tool for exploring GitHub organizations."


if __name__ == "__main__":
    mcp.run()
