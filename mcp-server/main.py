import asyncio
import os

from mcp_agent.app import MCPApp
from mcp_agent.agents.agent import Agent
from mcp_agent.workflows.llm.augmented_llm_openai import OpenAIAugmentedLLM

app = MCPApp(name="hello_world_agent")

async def call_agent(image_path: str, prompt: str):
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
                message="Change image so it is promoting the energy drink brand ZAPPED at file path boy.png use gen_image mcp api"
            )

            result = await llm.generate_str(
                message="Add the text: '50% discount if you show this image'. the image path is watermarked.png"
            )
            logger.info(f"the result for the llm is: {result}")
            return result


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
                message="Change image so it is promoting the energy drink brand ZAPPED at file path boy.png use gen_image mcp api"
            )

            result = await llm.generate_str(
                message="Add the text: '50% discount if you show this image'. the image path is watermarked.png"
            )

            logger.info(f"the result for the llm is: {result}")

if __name__ == "__main__":
    asyncio.run(example_usage())
