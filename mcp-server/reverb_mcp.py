# server.py
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print("add two numbers is working", a, b)
    return a + b * 2

@mcp.prompt
def summarize_request(text: str) -> str:
    """Generate a prompt asking for a summary."""
    return f"Please summarize the following text translating to french french:\n\n{text}"

if __name__ == "__main__":
    mcp.run()
