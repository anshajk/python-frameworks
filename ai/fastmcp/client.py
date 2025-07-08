import asyncio
import logging
from server import mcp

from fastmcp import Client

# Configure logging
from fastmcp.client.logging import LogMessage


logger = logging.getLogger("fastmcp.client")
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)


async def log_handler(message: LogMessage):
    log = logging.getLogger(message.logger or "server")
    level = getattr(logging, message.level.upper(), logging.INFO)
    log.log(level, message.data)


client = Client(mcp, log_handler=log_handler)


async def main():
    logger.info("Starting MCP client")

    try:
        async with client:
            logger.info("Client connected successfully")

            # Basic server interaction
            logger.debug("Sending ping to server")
            await client.ping()
            logger.info("Server ping successful")

            # List available operations
            logger.debug("Fetching available tools")
            tools = await client.list_tools()
            logger.info(f"Retrieved {len(tools) if tools else 0} tools")

            logger.debug("Fetching available resources")
            resources = await client.list_resources()
            logger.info(f"Retrieved {len(resources) if resources else 0} resources")

            logger.debug("Fetching available prompts")
            prompts = await client.list_prompts()
            logger.info(f"Retrieved {len(prompts) if prompts else 0} prompts")

            logger.info(f"Available Tools: {tools}")
            logger.info("-" * 180)
            logger.info(f"Available Resources: {resources}")
            logger.info("-" * 180)
            logger.info(f"Available Prompts: {prompts}")

            # Execute operations
            logger.debug("Calling example_tool with params: {'param': 'value'}")
            result = await client.call_tool("calculate_sum", {"a": 1, "b": 2})
            logger.info(f"Tool execution result: {result}")
            # print(result)

    except Exception as e:
        logger.error(f"Error during client execution: {e}", exc_info=True)
        raise
    finally:
        logger.info("MCP client shutting down")


if __name__ == "__main__":
    logger.info("MCP client script started")
    asyncio.run(main())
