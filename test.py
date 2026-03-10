import asyncio
import os
from langchain_mcp_adapters.client import MultiServerMCPClient  
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file    

async def main():
    github_mcp_pat = os.getenv("GITHUB_MCP_PAT")
    if not github_mcp_pat:
        raise ValueError("Missing GITHUB_MCP_PAT environment variable.")

    client = MultiServerMCPClient(
        {
            # "weather": {
            #     "transport": "http",  # HTTP-based remote server
            #     # Ensure you start your weather server on port 8000
            #     "url": "http://localhost:8000/mcp",
            # },
            "github": {
                "transport": "http",
                "url": "https://api.githubcopilot.com/mcp/",
                "headers": {
                    "Authorization": f"Bearer {github_mcp_pat}"
                },
            },
        }
    )

    tools = await client.get_tools()
    agent = create_agent(
        "openai:gpt-5.2",
        tools  
    )
    # weather_response = await agent.ainvoke(
    #     {"messages": [{"role": "user", "content": "How many repos are there in my github account?"}]}
    # )
    # print(weather_response["messages"][-1].content)
    return agent

if __name__ == "__main__":
    asyncio.run(main())