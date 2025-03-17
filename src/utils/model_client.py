from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

from src.core.settings import settings


def get_azure_openai_chat_completion_model_client() -> AzureOpenAIChatCompletionClient:
    """Get an Azure OpenAI chat completion model client.

    :return: AzureOpenAIChatCompletionClient
    """
    return AzureOpenAIChatCompletionClient(
        model=settings.AZURE_OPENAI.MODEL,
        api_key=settings.AZURE_OPENAI.API_KEY.get_secret_value(),
        azure_endpoint=settings.AZURE_OPENAI.ENDPOINT,
        api_version=settings.AZURE_OPENAI.API_VERSION,
    )
