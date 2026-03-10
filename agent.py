import asyncio
import os
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

_prompt_path = os.path.join(os.path.dirname(__file__), "system_prompt.md")
with open(_prompt_path, "r", encoding="utf-8") as _f:
    system_prompt = _f.read()


async def main():
    client = MultiServerMCPClient(
        {
            # "ado": {
            #     "command": "npx",
            #     "args": [
            #         "-y",
            #         "@azure-devops/mcp@next",
            #         os.getenv("ADO_ORGANIZATION"),
            #         "-d",
            #         "core",
            #         "work",
            #         "work-items",
            #         "search",
            #         "--authentication",
            #         "env",
            #     ],
            #     "transport": "stdio",
            # },
                        "github": {
                "transport": "http",
                "url": "https://api.githubcopilot.com/mcp/",
                "headers": {
                    "Authorization": f"Bearer {os.getenv("GITHUB_MCP_PAT")}"
                },
            }
        }
        )
    

    tools = await client.get_tools()
    agent = create_agent(
        model="openai:gpt-5.2",
        tools=tools,
        system_prompt=system_prompt
    )

    return agent


if __name__ == "__main__":
    asyncio.run(main())