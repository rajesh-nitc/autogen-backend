from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_core.model_context import BufferedChatCompletionContext

from src.tools.api_weather_tool import (
    get_location_coordinates_tool,
    get_weather_by_coordinates_tool,
)
from src.tools.vector_search_tool import get_vector_search_tool
from src.utils.model_client import get_azure_openai_chat_completion_model_client


async def get_team() -> SelectorGroupChat:
    """Create a team of agents for the task."""
    vector_search_agent = AssistantAgent(
        name="VectorSearchAgent",
        description="An agent for searching company policies, health plans, benefits.",
        model_client=get_azure_openai_chat_completion_model_client(),
        tools=[
            get_vector_search_tool,
        ],
        system_message="""You are a helpful assistant.
        Read all documents.
        Identify relevant content for the question.
        Answer the question using relevant information from the documents.
        Mention source, page_label only for docs that contributed to the answer.
        Return the answer in JSON format:
        {
            "answer": "<answer>",
            "sources": [
                {
                    "source": "<source>",
                    "page_label": <page_label>
                }
            ]
        }
        After the task is complete, respond with "TERMINATE".
        """,
        model_context=BufferedChatCompletionContext(buffer_size=25),
    )

    weather_agent = AssistantAgent(
        name="WeatherAgent",
        description="An agent for getting weather information.",
        model_client=get_azure_openai_chat_completion_model_client(),
        tools=[
            get_location_coordinates_tool,
            get_weather_by_coordinates_tool,
        ],
        system_message="""
        You are a helpful assistant. 
        After the task is complete, respond with "TERMINATE".
        """,
        model_context=BufferedChatCompletionContext(buffer_size=25),
    )

    text_mention_termination = TextMentionTermination("TERMINATE")
    max_messages_termination = MaxMessageTermination(max_messages=25)
    termination_condition = text_mention_termination | max_messages_termination

    team = SelectorGroupChat(
        [vector_search_agent, weather_agent],
        model_client=get_azure_openai_chat_completion_model_client(),
        termination_condition=termination_condition,
        allow_repeated_speaker=True,
    )
    return team
