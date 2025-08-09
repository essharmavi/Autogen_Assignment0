from autogen_ext.models.openai import OpenAIChatCompletionClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_model():
    model_client = OpenAIChatCompletionClient(
        model = "gpt-4o",
        api_key=os.getenv("OPENAI_API_KEY")
        )
    return model_client