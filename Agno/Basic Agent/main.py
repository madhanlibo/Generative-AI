from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
import os
from dotenv import load_dotenv
load_dotenv()

agent = Agent(
    model = Gemini(id="gemini-2.5-flash-preview-05-20"),
    description = "You are a financial agent, please reply based on the query",
    tools = [DuckDuckGoTools()],
    markdown = True
)

agent.print_response("What is nvidia currently investing in",stream=True)