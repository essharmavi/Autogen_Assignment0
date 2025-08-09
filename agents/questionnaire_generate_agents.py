from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from autogen_core.tools import FunctionTool
from autogen_agentchat.messages import StructuredMessage
from autogen_agentchat.ui import Console
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.pydantic_model import Questionnaire, JobDescription
from model.model import get_model
from prompts.prompts import agent_prompts
from tools.pdf_generator import questionnaire_to_pdf
import asyncio


def create_questionnaire_agent():
    agent = AssistantAgent(
        name="create_questionnaire_agent",
        model_client=get_model(),
        system_message=agent_prompts["create_questionnaire_agent"],
        description="Reads a Job Description from PDFResponse's class job_description attribute and creates a questionnaire based on it.",
        output_content_type=Questionnaire,
    )
    return agent


def questionnaire_to_pdf_agent():
    questionnaire_pdf_tool = FunctionTool(
        questionnaire_to_pdf,
        name="generate_pdf_from_questionnaire",
        description="Generates a PDF file from a given questionnaire text and saves it to disk.",
    )

    agent = AssistantAgent(
        name="questionnaire_to_pdf_agent",
        model_client=get_model(),
        description="Converts a questionnaire text into a downloadable PDF.",
        system_message=agent_prompts["questionnaire_to_pdf_agent"],
        tools=[questionnaire_pdf_tool],
    )
    return agent
