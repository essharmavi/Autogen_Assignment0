from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_core.tools import FunctionTool
from autogen_agentchat.ui import Console
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.pydantic_model import JobDescription, Questionnaire
from model.model import get_model
from tools.pdf_generator import get_jd_pdf
from prompts.prompts import agent_prompts
import asyncio


def jd_agent():
    agent = AssistantAgent(
        name="JD_Creator",
        model_client=get_model(),
        description="Creates a job description based on the provided requirements.",
        system_message=agent_prompts["JD_Creator"],
        output_content_type=JobDescription,
    )
    return agent


def user_agent():
    agent = UserProxyAgent(
        name="user_agent", description="A human user", input_func=input
    )
    return agent


def editor_agent():
    agent = AssistantAgent(
        name="JD_Editor",
        model_client=get_model(),
        description="Edits the JD based on the user's input and JD_Creator output",
        system_message=agent_prompts["JD_Editor"],
        output_content_type=JobDescription,
    )
    return agent


def pdf_agent():
    pdf_tool = FunctionTool(
        get_jd_pdf,
        name="generate_pdf_from_jd",
        description="Generates a PDF file from the given JobDescription and saves it to disk.",
    )

    agent = AssistantAgent(
        name="jd_to_pdf_agent",
        model_client=get_model(),
        description="A helpful agent that converts a Job Description into a downloadable PDF.",
        system_message=agent_prompts["jd_to_pdf_agent"],
        tools=[pdf_tool],
    )
    return agent
