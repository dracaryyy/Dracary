import json
import httpx
from typing import Any
from dracary.agent.dracary import Dracary
from mcp.server.fastmcp import FastMCP

# Initialize Dracary MCP Server
mcp = FastMCP("Dracary")

# Initialize Dracary Agent
dracary_agent = Dracary()

@mcp.tool()
async def query_dracary(input: str) -> str:
    # Get the task description from the console input
    user_prompt = input("Please enter the task description：\n")
    dracary_agent = Dracary()

    # Generate reason
    print("=== REASONING PHASE ===")
    reason = await dracary_agent.reason(user_prompt)
    print(f"Generated Plan: {reason}")  # Output the generated plan
    
    # Excute action
    print("\n=== SAVING PLAN TO FILE ===")
    result = await dracary_agent.action(reason, file_path="plan.txt")
    print("\nThe task plan has been saved. The result is as follows:")
    return result

if __name__ == "__main__":
    # Run the Dracary MCP Server using standard I/O
    mcp.run(transport='stdio')