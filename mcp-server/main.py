import asyncio
import os

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM

app = MCPApp(name="hello_world_agent")

async def example_usage():
    async with app.run() as mcp_agent_app:
        logger = mcp_agent_app.logger
        # This agent can read the filesystem or fetch URLs
        finder_agent = Agent(
            name="finder",
            instruction="""You can read local files or fetch URLs.
                Return the requested information when asked.""",
            server_names=["reverb-ai-image-editor"], # MCP servers this Agent can use
        )

        async with finder_agent:
            # Automatically initializes the MCP servers and adds their tools for LLM use
            tools = await finder_agent.list_tools()
            logger.info(f"Tools available:", data=tools)

            # Attach an OpenAI LLM to the agent (defaults to GPT-4o)
            llm = await finder_agent.attach_llm(OpenAIAugmentedLLM)

            # This will perform a file lookup and read using the filesystem server
            result = await llm.generate_str(
                message="add 55 and the number sixteen"
            )
            logger.info(f"the result for the llm is: {result}")

            # Uses the fetch server to fetch the content from URL
            result = await llm.generate_str(
                message="summarize the following text:\n\nWhile similar capabilities can be implemented with asyncio in-memory execution, Temporal provides these features out-of-the-box and is recommended for production deployments."
            )
            logger.info(f"summary: {result}")

if __name__ == "__main__":
    asyncio.run(example_usage())
