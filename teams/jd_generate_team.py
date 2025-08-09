from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
from autogen_agentchat.messages import (
    BaseAgentEvent,
    BaseChatMessage,
    StructuredMessage,
)
from autogen_core.tools import FunctionTool
from typing import Sequence
from autogen_agentchat.ui import Console
import os
import sys
import asyncio

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.pydantic_model import JobDescription
from model.model import get_model
from prompts.prompts import agent_prompts
from agents.jd_generate_agents import user_agent, jd_agent, editor_agent, pdf_agent


def selector_func(messages: Sequence[BaseAgentEvent | BaseChatMessage]) -> str | None:
    if len(messages) == 1:
        # First message — start with JD_Creator
        return jd_agent().name

    last_msg = messages[-1]
    second_last_msg = messages[-2] if len(messages) >= 2 else None

    # Rule 1: Stop everything if PDF agent has responded
    if last_msg.source == pdf_agent().name:
        return None

    # Rule 2: After JD_Creator, expect user response
    if last_msg.source == jd_agent().name:
        return user_agent().name

    # Rule 3: After user response to JD, go to PDF if approved, else to editor
    if (
        second_last_msg
        and second_last_msg.source == jd_agent().name
        and last_msg.source == user_agent().name
    ):
        if any(word in last_msg.content.upper() for word in ["APPROVE", "APPROVED"]):
            return pdf_agent().name
        else:
            return editor_agent().name

    # Rule 4: After Editor, prompt user again
    if (
        second_last_msg
        and second_last_msg.source == editor_agent().name
        and last_msg.source == user_agent().name
    ):
        if any(word in last_msg.content.upper() for word in ["APPROVE", "APPROVED"]):
            return pdf_agent().name
        else:
            return editor_agent().name

    # Rule 5: After editor updates, go back to user
    if last_msg.source == editor_agent().name:
        return user_agent().name

    return None


async def run_jd_generate_team(task: str):
    print("I am running run_jd_generate_team")
    team = SelectorGroupChat(
        participants=[jd_agent(), editor_agent(), pdf_agent(), user_agent()],
        name="JD_creator_team",
        termination_condition=TextMentionTermination("TERMINATE VAGUE QUERY")
        | TextMentionTermination("TERMINATE BY EDITOR- JD NOT APPROVED")
        | TextMentionTermination("TERMINATE"),
        custom_message_types=[StructuredMessage[JobDescription]],
        selector_prompt=agent_prompts["selector_prompt"],
        allow_repeated_speaker=True,
        selector_func=selector_func,
        model_client=get_model(),
        max_turns=10,
    )
    return team
