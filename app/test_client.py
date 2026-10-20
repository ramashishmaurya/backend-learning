import asyncio
from fastmcp import Client

async def main():
    # 1. Apne chal rahe HTTP server se connect karo
    async with Client("http://127.0.0.1:8000/mcp") as client:
        # 2. Server se pucho tumhare paas kaunse tools hain
        tools = await client.list_tools()
        print("Available tools:", [t.name for t in tools])

        # 3. Tool ko call karo
        result = await client.call_tool("get_weather", {"city": "Mumbai"})
        print("Response from server:", result)

if __name__ == "__main__":
    asyncio.run(main())
