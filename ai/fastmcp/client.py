import asyncio

import logging
from server import mcp


from fastmcp import Client


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

    logger.info("Starting MCP Client")

    try:
        async with client:
            logger.info("Client connected successfully")
            logger.debug("Sending ping to server")
            await client.ping()
            logger.info("Server ping successful")

            logger.debug("Fetching available tools")
            tools = await client.list_tools()
            logger.info(f"Retrieved {len(tools) if tools else 0}")

            resources = await client.list_resources()
            logger.info(f"Retrieved {len(resources) if resources else 0}")

            prompts = await client.list_prompts()
            logger.info(f"Retrieved {len(prompts) if prompts else 0}")

            logger.info(f"Available tools: {tools}")
            logger.info("-" * 180)
            logger.info(f"Available resources: {resources}")
            logger.info("-" * 180)
            logger.info(f"Available prompts: {prompts}")
            logger.info("-" * 180)

            result = await client.call_tool("get_latest_spacex_launch")
            logger.info(f"Tool execution result: {result}")

    except Exception as e:
        logger.error(f"Error during client execution: {e}", exc_info=True)
        raise
    finally:
        logger.info("MCP client shutting down")


if __name__ == "__main__":
    logger.info("MCP client script started")
    asyncio.run(main())
