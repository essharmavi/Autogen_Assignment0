import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.pydantic_model import JobDescription, Questionnaire
from model.model import get_model
from tools.pdf_generator import get_jd_pdf
from prompts.prompts import agent_prompts
import asyncio
from autogen_agentchat.messages import StructuredMessage
from agents.society_of_mind_agent import society_of_mind_agent
from autogen_agentchat.teams import SelectorGroupChat
from agents.questionnaire_generate_agents import (
    create_questionnaire_agent,
    questionnaire_to_pdf_agent,
)
from agents.jd_generate_agents import user_agent
from autogen_agentchat.conditions import TextMentionTermination, MaxMessageTermination
from autogen_agentchat.messages import (
    BaseAgentEvent,
    BaseChatMessage,
    StructuredMessage,
)
from typing import Sequence


def selector_func(messages: Sequence[BaseAgentEvent | BaseChatMessage]) -> str | None:
    last_msg = messages[-1]

    if last_msg.source == "Get_JD_SOM":
        return create_questionnaire_agent().name

    if last_msg.source == user_agent().name:
        text = last_msg.content.lower()
        if "approve" in text or "approved" in text:
            return questionnaire_to_pdf_agent().name
        else:
            return create_questionnaire_agent().name

    if last_msg.source == create_questionnaire_agent().name:
        return user_agent().name

    if last_msg.source == questionnaire_to_pdf_agent().name:
        return None

    return None


async def questionnaire_generator_team(task: str):
    print("I am running questionnaire_generator_team")
    som_agent = await society_of_mind_agent(task)
    team = SelectorGroupChat(
        participants=[
            som_agent,
            create_questionnaire_agent(),
            user_agent(),
            questionnaire_to_pdf_agent(),
        ],
        name="Get_Questionnarie_from_JD",
        description="Get Questionnaire form JD",
        custom_message_types=[
            StructuredMessage[Questionnaire],
            StructuredMessage[JobDescription],
        ],
        max_turns=10,
        termination_condition=TextMentionTermination("TERMINATE"),
        model_client=get_model(),
        selector_func=selector_func,
    )
    return team
