from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from posthog import privacy_mode

from apps.entities.chat_models.chat_models import base_chat
from langchain.agents.tool_calling_agent.base import create_tool_calling_agent
from langchain_mcp_adapters.tools import load_mcp_tools

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)

from langchain.agents.agent_types import AgentType


# Optional: create a sampling callback
async def handle_sampling_message(
    message: types.CreateMessageRequestParams,
) -> types.CreateMessageResult:
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text="Hello, world! from model",
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )


from langgraph.prebuilt import create_react_agent


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write, sampling_callback=handle_sampling_message
        ) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools = await load_mcp_tools(session)
            print(tools)
            resources = await session.list_resources()
            agent = create_react_agent(base_chat, tools)
            print(await agent.ainvoke({"messages": "일본 수도 알려줘 "}))
            print(await session.read_resource(resources.resources[0].uri))


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
