from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_core.model_context import BufferedChatCompletionContext

from src.core.settings import settings
from src.tools.api_weather_tool import (
    get_location_coordinates_tool,
    get_weather_by_coordinates_tool,
)
from src.tools.vector_search_tool import get_vector_search_tool
from src.utils.model_client import get_azure_openai_chat_completion_model_client


async def get_single_agent_team() -> RoundRobinGroupChat:
    """Get a team with a single agent.

    :return: RoundRobinGroupChat
    """
    assistant = AssistantAgent(
        name="assistant",
        model_client=get_azure_openai_chat_completion_model_client(),
        tools=[
            get_location_coordinates_tool,
            get_weather_by_coordinates_tool,
            get_vector_search_tool,
        ],
        system_message="You are a helpful assistant.",
        model_context=BufferedChatCompletionContext(
            buffer_size=settings.LLM.LAST_N_MESSAGES_TO_LLM
        ),
    )
    termination_condition = TextMessageTermination("assistant")
    team = RoundRobinGroupChat(
        [assistant],
        termination_condition=termination_condition,
    )
    return team
