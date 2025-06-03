from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools

import os
from dotenv import load_dotenv
load_dotenv()

web_agent = Agent(
    name = "Web Agent",
    role = "Search the web for the information",
    model = Gemini(id="gemini-2.5-flash-preview-05-20"),
    tools = [DuckDuckGoTools()],
    instructions = "Always include the source",
    show_tool_calls = True,
    markdown = True
)

finance_agent=Agent(
    name = "Finance Agent",
    role = "Get Financial data",
    model = Gemini(id="gemini-2.5-flash-preview-05-20"),
    tools = [YFinanceTools(stock_price=True,analyst_recommendations=True,stock_fundamentals=True,company_info=True)],
    show_tool_calls = True,
    markdown = True
)

agent_team=Agent(
    team = [web_agent, finance_agent],
    model = Gemini(id="gemini-2.5-flash-preview-05-20"),
    instructions = ["Always include sources", "use tables to display data", "Always use tools"],
    show_tool_calls = True,
    markdown = True
)

agent_team.print_response("what is recent development in Google AI?",stream=True)
