import json
import os

import aiofiles
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.model_context import BufferedChatCompletionContext

from src.tools.weather_tool import get_location_coordinates, get_weather_by_coordinates
from src.utils.model_client import get_azure_openai_chat_completion_model_client

state_path = "team_state.json"


# Team with one agent
async def get_single_agent_team() -> RoundRobinGroupChat:

    assistant = AssistantAgent(
        name="assistant",
        model_client=get_azure_openai_chat_completion_model_client(),
        tools=[get_location_coordinates, get_weather_by_coordinates],
        system_message="You are a helpful assistant.",
        model_context=BufferedChatCompletionContext(buffer_size=5),
    )

    termination_condition = TextMessageTermination("assistant")

    team = RoundRobinGroupChat(
        [assistant],
        termination_condition=termination_condition,
    )

    # Load state from file.
    if not os.path.exists(state_path):
        return team
    async with aiofiles.open(state_path, "r") as file:
        state = json.loads(await file.read())
    await team.load_state(state)
    return team
