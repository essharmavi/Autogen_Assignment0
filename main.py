from teams.questionnaire_generator_team import questionnaire_generator_team
from autogen_agentchat.ui import Console
import asyncio


async def main(task: str):
    team = await questionnaire_generator_team(task=task)
    await Console(team.run_stream(task=task))


if __name__ == "__main__":
    task = "Create a JD for Gen AI developer with 5 years of experience. Location New Delhi. Company Microsoft."
    asyncio.run(main(task=task))
