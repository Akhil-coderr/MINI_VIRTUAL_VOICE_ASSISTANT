from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    google,
    noise_cancellation,
)
from prompt import AGENT_INSTRUCTIONS, AGENT_RESPONSE
load_dotenv()


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions=AGENT_INSTRUCTIONS)


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=google.beta.realtime.RealtimeModel(
        model="gemini-2.0-flash-exp",
        voice="Aoede",
        temperature=0.8,
        instructions=AGENT_INSTRUCTIONS,
    )
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
            video_enabled=True
        ),
    )

    await session.generate_reply(
        instructions=AGENT_RESPONSE,
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
# This is a simple example of how to create a voice assistant using LiveKit Agents.
# To run this example, you need to have the LiveKit Python SDK installed and set up

# to start my assistant: (check if venv file is activated if not then)
# Make sure to set the environment variables for your LiveKit credentials.
# You can run this script from the command line:
#               python agent.py console

# to activate venv:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
# .\venv\Scripts\Activate.ps1

# to connect to a background room:

#https://agents-playground.livekit.io/
#python agent.py dev
# to close  CTRL + C