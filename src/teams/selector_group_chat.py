from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_core.model_context import BufferedChatCompletionContext

from src.tools.vector_search_tool import get_vector_search_tool
from src.tools.weather_tool import (
    get_location_coordinates_tool,
    get_weather_by_coordinates_tool,
)
from src.utils.model_client import get_azure_openai_chat_completion_model_client

TERMINATION_TEXT = "TERMINATE"
BUFFER_SIZE = 25
MAX_MESSAGES = 25

model_client = get_azure_openai_chat_completion_model_client()


async def get_team() -> SelectorGroupChat:
    """Create a team of agents for the task."""
    benefits_agent = AssistantAgent(
        name="BenefitsAgent",
        description="Answers questions about employee benefits, including health plans and policies.",
        model_client=model_client,
        tools=[
            get_vector_search_tool,
        ],
        system_message=f"""
        You are a helpful assistant.
        Answer questions using relevant information from the provided documents.
        Only cite documents (via `source` and `page_label`) that directly contributed to the answer.
        The content of the documents will be provided to you along with their source and page_label metadata.
        Respond in the following JSON format:
        {{
            "answer": "<answer>",
            "sources": [
                {{
                    "source": "<source>",
                    "page_label": <page_label>
                }}
            ]
        }}
        After completing the task, respond with {TERMINATION_TEXT}.
        """,
        model_context=BufferedChatCompletionContext(buffer_size=BUFFER_SIZE),
    )

    weather_agent = AssistantAgent(
        name="WeatherAgent",
        description="Retrieves weather information based on location.",
        model_client=model_client,
        tools=[
            get_location_coordinates_tool,
            get_weather_by_coordinates_tool,
        ],
        system_message=f"""
        You are a helpful assistant. 
        After completing the task, respond with {TERMINATION_TEXT}.
        """,
        model_context=BufferedChatCompletionContext(buffer_size=BUFFER_SIZE),
    )

    termination_condition = TextMentionTermination(TERMINATION_TEXT) | MaxMessageTermination(max_messages=MAX_MESSAGES)

    team = SelectorGroupChat(
        [benefits_agent, weather_agent],
        model_client=model_client,
        termination_condition=termination_condition,
        allow_repeated_speaker=True,
    )
    return team
