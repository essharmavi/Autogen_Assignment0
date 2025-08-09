from autogen_agentchat.agents import SocietyOfMindAgent
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from teams.jd_generate_team import run_jd_generate_team
from model.model import get_model


async def society_of_mind_agent(task):
    print("I am running Society fo Mind Agent")
    jd_generate_team = await run_jd_generate_team(task)
    agent = SocietyOfMindAgent(
        name="Get_JD_SOM",
        team=jd_generate_team,
        model_client=get_model(),
        description="Get the Job Description",
    )

    return agent
