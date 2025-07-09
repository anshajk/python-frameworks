from fastmcp import FastMCP, Context

import aiohttp
import ssl
import json
from typing import Dict, Any


mcp = FastMCP(
    name="SpaceX API server",
    instructions="This server can be used for accessing SpaceX launch data",
    version="1.0.0",
    dependencies=["aiohttp"],
)


def create_ssl_context():
    """Create an SSL context that bypasses certificate verification."""
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    return ssl_context


@mcp.tool()
async def get_latest_spacex_launch(context: Context) -> Dict[str, Any]:
    """Fetch the latest SpaceX launch data from the SpaceX API."""
    await context.info("Fetching latest SpaceX launch data...")

    try:
        ssl_context = create_ssl_context()
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(
                "https://api.spacexdata.com/v5/launches/latest"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    await context.info("Successfully fetched latest launch data")
                    return data
                else:
                    await context.error(f"Failed to fetch data: HTTP {response.status}")
                    return {"error": f"HTTP {response.status}"}
    except Exception as e:
        await context.error(f"Error fetching SpaceX data: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
async def get_spacex_launch_by_id(launch_id: str, context: Context) -> Dict[str, Any]:
    """Fetch a specific SpaceX launch by its ID."""
    await context.info(f"Fetching SpaceX launch data for ID: {launch_id}")

    try:
        ssl_context = create_ssl_context()
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(
                f"https://api.spacexdata.com/v5/launches/{launch_id}"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    await context.info(
                        f"Successfully fetched launch data for {launch_id}"
                    )
                    return data
                else:
                    await context.error(f"Failed to fetch data: HTTP {response.status}")
                    return {"error": f"HTTP {response.status}"}
    except Exception as e:
        await context.error(f"Error fetching SpaceX data: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
async def get_upcoming_spacex_launches(context: Context) -> Dict[str, Any]:
    """Fetch upcoming SpaceX launches."""
    await context.info("Fetching upcoming SpaceX launches...")

    try:
        ssl_context = create_ssl_context()
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(
                "https://api.spacexdata.com/v5/launches/upcoming"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    await context.info(
                        f"Successfully fetched {len(data)} upcoming launches"
                    )
                    return {"launches": data, "count": len(data)}
                else:
                    await context.error(f"Failed to fetch data: HTTP {response.status}")
                    return {"error": f"HTTP {response.status}"}
    except Exception as e:
        await context.error(f"Error fetching SpaceX data: {str(e)}")
        return {"error": str(e)}


@mcp.tool()
async def search_spacex_launches(
    context: Context,
    rocket_name: str = None,
    mission_patch: bool = None,
    success: bool = None,
    limit: int = 10,
) -> Dict[str, Any]:
    """Search SpaceX launches with optional filters."""
    await context.info(f"Searching SpaceX launches with filters...")

    try:
        # Build query parameters
        query = {"limit": limit}

        if rocket_name:
            query["rocket"] = rocket_name
        if mission_patch is not None:
            query["links.patch.small"] = {"$exists": mission_patch}
        if success is not None:
            query["success"] = success

        # Use the query endpoint for more advanced searching
        ssl_context = create_ssl_context()
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.post(
                "https://api.spacexdata.com/v5/launches/query",
                json={"query": query, "options": {"limit": limit}},
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    await context.info(
                        f"Found {len(data.get('docs', []))} matching launches"
                    )
                    return data
                else:
                    await context.error(f"Failed to search: HTTP {response.status}")
                    return {"error": f"HTTP {response.status}"}
    except Exception as e:
        await context.error(f"Error searching SpaceX launches: {str(e)}")
        return {"error": str(e)}


# SpaceX resource to provide launch data as a resource
@mcp.resource("spacex://launches/latest")
async def spacex_latest_launch_resource():
    """Provide latest SpaceX launch as a resource."""
    try:
        ssl_context = create_ssl_context()
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(
                "https://api.spacexdata.com/v5/launches/latest"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return json.dumps(data, indent=2)
                else:
                    return f"Error: HTTP {response.status}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.resource("spacex://launches/{launch_id}")
async def spacex_launch_resource(launch_id: str):
    """Provide specific SpaceX launch data as a resource."""
    try:
        ssl_context = create_ssl_context()
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(
                f"https://api.spacexdata.com/v5/launches/{launch_id}"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return json.dumps(data, indent=2)
                else:
                    return f"Error: HTTP {response.status}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.resource("spacex://rockets/list")
def spacex_rockets_list():
    """Provide a static list of SpaceX rockets as a resource."""
    rockets = {
        "rockets": [
            {
                "id": "falcon1",
                "name": "Falcon 1",
                "type": "rocket",
                "active": False,
                "stages": 2,
                "boosters": 0,
                "cost_per_launch": 6700000,
                "success_rate_pct": 40,
                "first_flight": "2006-03-24",
                "country": "Republic of the Marshall Islands",
                "company": "SpaceX",
                "height": {"meters": 22.25, "feet": 73},
                "diameter": {"meters": 1.68, "feet": 5.5},
                "mass": {"kg": 30146, "lb": 66460},
                "description": "The Falcon 1 was an expendable launch system privately developed and manufactured by SpaceX during 2006-2009.",
            },
            {
                "id": "falcon9",
                "name": "Falcon 9",
                "type": "rocket",
                "active": True,
                "stages": 2,
                "boosters": 0,
                "cost_per_launch": 62000000,
                "success_rate_pct": 97,
                "first_flight": "2010-06-04",
                "country": "United States",
                "company": "SpaceX",
                "height": {"meters": 70, "feet": 229.6},
                "diameter": {"meters": 3.7, "feet": 12},
                "mass": {"kg": 549054, "lb": 1207920},
                "description": "Falcon 9 is a reusable, two-stage rocket designed and manufactured by SpaceX for the reliable and safe transport of people and payloads into Earth orbit and beyond.",
            },
            {
                "id": "falconheavy",
                "name": "Falcon Heavy",
                "type": "rocket",
                "active": True,
                "stages": 2,
                "boosters": 2,
                "cost_per_launch": 97000000,
                "success_rate_pct": 100,
                "first_flight": "2018-02-06",
                "country": "United States",
                "company": "SpaceX",
                "height": {"meters": 70, "feet": 229.6},
                "diameter": {"meters": 12.2, "feet": 39.9},
                "mass": {"kg": 1420788, "lb": 3125735},
                "description": "With the ability to lift into orbit over 54 metric tons (119,000 lb)--a mass equivalent to a 737 jetliner loaded with passengers, crew, luggage and fuel--Falcon Heavy can lift more than twice the payload of the next closest operational vehicle, the Delta IV Heavy.",
            },
            {
                "id": "starship",
                "name": "Starship",
                "type": "rocket",
                "active": False,
                "stages": 2,
                "boosters": 0,
                "cost_per_launch": 10000000,
                "success_rate_pct": 0,
                "first_flight": "2023-04-20",
                "country": "United States",
                "company": "SpaceX",
                "height": {"meters": 120, "feet": 394},
                "diameter": {"meters": 9, "feet": 30},
                "mass": {"kg": 5000000, "lb": 11023113},
                "description": "Starship is a fully reusable transportation system designed to carry both crew and cargo to Earth orbit, the Moon, Mars and beyond.",
            },
        ],
        "total_count": 4,
        "active_count": 2,
        "retired_count": 1,
        "in_development_count": 1,
    }
    return json.dumps(rockets, indent=2)


@mcp.prompt("spacex_launch_summary")
def spacex_launch_summary(launch_data: str) -> str:
    """Generate a summary of a SpaceX launch from the provided data"""
    return (
        f"Please provide a detailed summary of this SpaceX launch data: {launch_data}"
    )


@mcp.prompt("spacex_mission_analysis")
def spacex_mission_analysis(mission_name: str) -> str:
    """Generate an analysis prompt for a specific SpaceX mission"""
    return f"Analyze the SpaceX mission '{mission_name}' including its objectives, outcomes, and significance in space exploration history."


if __name__ == "__main__":
    mcp.run()
